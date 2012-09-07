if request.env.web2py_runtime_gae:            
# if running on Google App Engine
    db = DAL('gae')                           
# connect to Google BigTable
    session.connect(request, response, db=db) 
# and store sessions and tickets there
else:                                         
# else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       
# if not, use SQLite or other DB
from gluon.tools import *
auth=Auth(globals(),db)                      
# authentication/authorization
auth.settings.hmac_key='sha512:40b75704-2d17-4fe6-9e58-2d33a13a5d59'
auth.define_tables()                         
# creates all needed tables
crud=Crud(globals(),db)                      
# for CRUD helpers using auth
service=Service(globals())                  
# for json, xml, jsonrpc, xmlrpc, amfrpc

db.define_table('picture',
		SQLField('pic','upload', requires=IS_NOT_EMPTY()),
                SQLField('use' , db.auth_user , default=auth.user_id, writable=False, requires= IS_IN_DB(db,db.auth_user.id)))

db.define_table('music',                     	
		# creates table with name music
                SQLField('name'),		
		# entity name	
                SQLField('genre'),		
		# entity genre
                SQLField('artist'),		
		# entity artist
                SQLField('album'),		
		# entity album	
                SQLField('language'),		
		# entity language	
                SQLField('rating','integer'),	
		# field for rating on a scale of 1 to 5
                SQLField('song', 'upload'))  	
		# upload feature for selected song  



""" the above db table is the core of the application developed, only a single table has been used to develop the entire application. Functionalities like- 
    
a)Searching for songs in accordance with above fields 
    
b)Viewing all the songs
    
c)Adding new songs with the aforesaid mentioned criteria
    
d)deletion of a song 
    
e)developing an open source platform for song sharing
    
f)seperate user id and password for the contributors
    
g)playing a particular song online
    
h)main page will show latest updates, top-rated songs, recently played, recently added songs
    
i)providing download to registered and even unregistered users               
"""



db.music.name.requires=IS_NOT_EMPTY()
#name of song should not be left empty so that it can be found easily later
db.music.song.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,db.music.song)]
#empty uploads disallowed and repeated entries forbidden
db.music.genre.requires=IS_IN_SET(['blues','alternative','jazz','rock','metal','pop','retro','r&b','rap','classical','gazal','ska','punk','hip-hop','hardcore','gothic','sufi','opera','techno','folk','other'])
#genre should be an entity of the set given alongside
db.music.album.requires=IS_NOT_EMPTY()
#album field shouldnt be left although multiple songs can be of the same album
db.music.rating.requires = IS_IN_SET(range(0,6))
#rating by the user on a scale of 0-5
db.music.language.requires=IS_IN_SET(['english','hindi','telugu','tamil','bengali','malayalam','spanish','italian','russian','swiss','mandarin','japanese','african','korean','arabic','other european','other asian','latin american','other'])
#music language is required for the convenience users listening to particular language, it wud be an entity of set given alongside
db.music.artist.requires=IS_NOT_EMPTY()
#artist field shouldnt be left empty


import datetime


db.define_table('comment', 	
		# defines a table with name comment
		# used to comment on a song
                SQLField('comment','text', requires=IS_NOT_EMPTY()),	
		# entity or SQLField comment with data type text
                SQLField('user' , db.auth_user , default=auth.user_id, writable=False, requires= IS_IN_DB(db,db.auth_user.id)), 
		#user and the restrictions pertaining to the person logged in.	0000000
                SQLField('music', db.music, requires=IS_IN_DB(db,db.music.id, '%(name)s')))
		#the song should be present in the database.

db.define_table('playlist',
		#SQLField('Playlist','string',requires=IS_NOT_EMPTY),

		SQLField('Song',db.music,requires=IS_IN_DB(db,db.music.id,'%(name)s')),
		#for the song to be in the playlist it must necessarily be a part of the universal database.		
		SQLField('User_id',db.auth_user, default=auth.user_id, writable=False, requires = IS_IN_DB(db,db.auth_user.id)))
		#playlist must be user affiliated.

db.define_table('abuse',
		#defines a table by the name 'abuse'		
		SQLField('song', db.music, requires= IS_IN_DB(db, db.music.id, '%(name)s')),
		#for abuse to be reported, the song must be a part of the universal database
		SQLField('User', db.auth_user, default=auth.user_id, writable=False, requires=IS_IN_DB(db, db.auth_user.id)))
		#the abuse will be reported with the name of the user.
db.define_table('forum',
		#defines a table with the name 'forum'	
		SQLField('Comment','text',requires=IS_NOT_EMPTY()),
		#creates a field with name comment and data type text.
		SQLField('Users',db.auth_user, default=auth.user_id, writable=False, requires = IS_IN_DB(db,db.auth_user.id)))
		#creates a field with name users and gives the required restrictions.
