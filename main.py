from github import Github
import json
import asyncio

class DBError(Exception):
    def __init__(self,message):
        super().__init__(message)

class DBKirosake():
    def __init__(self,access_token,repository):
        self.access_token=access_token
        self.repository=repository
        self.repo=Github(access_token).get_repo(repository)
       # self.dataBase=0
        
        
    async def update(self,file,rows,datas,datatype,updtype,comm='update'):
        file_content=self.repo.get_contents(file)
        db=file_content.decoded_content.decode()
        db=json.loads(db)
        
        if datatype=='str':
            db[rows]=datas
            json_object=json.dumps(db,indent=4)

        elif datatype=='int':
            if updtype=='add':
                db[rows]+=int(datas)
                json_object=json.dumps(db,indent=4)
            elif updtype=='replace':
                db[rows]=int(datas)
                json_object=json.dumps(db,indent=4)
            
        elif datatype=='float':
            if updtype=='add':
                db[rows]+=float(datas)
                json_object=json.dumps(db,indent=4)
            elif updtype=='replace':
                db[rows]=float(datas)
                json_object=json.dumps(db,indent=4)
            
        file_content = self.repo.get_contents(file)
        json_object = json.dumps(db, indent = 4)
        self.repo.update_file(file_content.path,comm, json_object, file_content.sha)
        return db
    
    
    
    async def update_more(self,file,one,two,date,datatype,updtype,comm='update'):
        file_content=self.repo.get_contents(file)
        db=file_content.decoded_content.decode()
        db=json.loads(db)
        
        if date is None:
            return 'Date is None'
        else:
            
            if datatype=='str':
                db[one][two]=date
                    
            elif datatype=='int':
                if updtype=='add':
                    db[one][two]+=int(date)
                elif updtype=='take':
                    db[one][two]-=int(date)
                elif updtype=='replace':
                    db[one][two]=int(date)
                    
            elif datatype=='float':
                if updtype=='add':
                    db[one][two]+=float(date)
                elif updtype=='take':
                    db[one][two]-=float(date)
                elif updtype=='replace':
                    db[one][two]=float(date)
                    
            elif datatype=='list':
                if updtype=='add':
                    pass
                elif updtype=='replace':
                    pass
                    
            else:
                return 'ERROR search Data Type'
        
        json_object = json.dumps(db, indent = 4)
        self.repo.update_file(file_content.path,comm, json_object, file_content.sha)
        return db
        
    
    async def update_list(self,file,list):
        db=list
        json_object=json.dumps(db,indent=4)
        file_content = self.repo.get_contents(file)
        self.repo.update_file(file_content.path,'update', json_object, file_content.sha)
        return db
    
    async def get(self,file):
        file_content=self.repo.get_contents(file)
        db=file_content.decoded_content.decode()
        db=json.loads(db)
        return db
        
    async def create(self,file,content):
        self.repo.create_file(file,'init commit',content)
        return 'Create file {file.path}'
        
    async def name_files(self,file):
        contents = self.repo.get_contents(file)
        array_file=[]
        for content_file in contents:
            array_file.append(content_file.path)
        return array_file
    
    async def delete(self,file):
        self.repo.delete_file(file.path, "remove test", file.sha)
        return 'Delete file {file.path}'
        
        
    async def create_db(self,nameDB=None,folder=None,ids=None,database=None):
        if nameDB==None:
            raise DBError('Name database is not entered')
            return
        if folder==None:
            file=f'{str(nameDB)}/users.json'
        else:
            file=f'{str(nameDB)}/{str(folder)}/users.json'
        if ids==None:
            raise DBError('Folder to database file is not init')
            return
        if database==None:
            raise DBError('Content with database file is not')
            return
       
        try:
            file_content=self.repo.get_contents(file)
            db=file_content.decoded_content.decode()
            db=json.loads(db)
            if str(ids) in db:
                pass
            else:
                db[ids]=database
            json_object=json.dumps(db,indent=4)
            file_content = self.repo.get_contents(file)
            self.repo.update_file(file_content.path,'update', json_object, file_content.sha)
            return db
        except:
            db={}
            db[ids]=database
            json_object = json.dumps(db, indent = 4)
            self.repo.create_file(file,'init commit',json_object)
            return 'Create file {file.path}'