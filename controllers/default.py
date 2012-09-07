def index():#no explicit use, redirects to homepage or login page whichever is suitable
   	return dict(message=T(''))

#@auth.requires_login()
def user():
    return dict(form=auth()) 	
#provides login and defines class user, with limited access and authority.
#type of user extrapolates on the kind of access offered to the person logged in.
	#for example a normal user has access to basic functions in the website, end user interface based.
 	#user has access to 
	# 1. View all songs.
	# 2. Add songs.    
	# 3. User Settings.
	# 4. Comment on a song.
	# 5. View all comments.
	# 6. View playlist.
	# 7. Report Abuse.
	# 8. Forum.	    

def download():
#for providing download of files
    import os
    filename=os.path.join(request.folder,'uploads/','%s' % request.args[0])
    return response.stream(open(filename,'rb'))
	# allows for direct download of song if the user likes it.
	# download request is preceded by disclaimer which encourages user to buy and promote the music if he/she likes it.	

def play(): 
    #function aids in playing of the audio file.
    musics=db(request.args(0)==db.music.id).select(db.music.ALL)
    #musics=db().select(db.music.ALL, orderby=db.music.name)
    return dict(musics=musics)

@auth.requires_login()	
def navigate():
#provides smooth navigation
    return dict()

@auth.requires_membership('Admin')
def rep_abuse():
    music=db().select(db.abuse.ALL, orderby=db.abuse.song)
    musics=db().select(db.music.ALL, orderby=db.music.name)
    return dict(musics=musics,music=music)
	

@auth.requires_login()
def home():
    #homepage
    form = SQLFORM(db.picture)
    if form.accepts(request.vars):
        response.flash = 'Success!'
    elif form.errors:
        response.flash = 'Error adding new picture'
    
    pics=db().select(db.picture.ALL, orderby=db.picture.use)
    musics=db().select(db.music.ALL, orderby=db.music.name)
    return dict(pics=pics,musics=musics,form=form)
    #allows user to go to the home page.	

@auth.requires_login()
def add():
    #function provides the upload of songs
    #record= db.music(request.args(0)) or redirect(URL('index'))
    #url=URL('download')
    form = SQLFORM(db.music)
    if form.accepts(request.vars):
        response.flash = 'Success!'
    elif form.errors:
        response.flash = 'Error adding new music'
    
    return dict(form=form)

@auth.requires_login()
def add_pic():
    #function provides the upload of songs
    #record= db.music(request.args(0)) or redirect(URL('index'))
    #url=URL('download')
    form = SQLFORM(db.picture)
    if form.accepts(request.vars):
        response.flash = 'Success!'
    elif form.errors:
        response.flash = 'Error adding new music'
    return dict(form=form)

@auth.requires_membership('Admin')	
#defines user with administrative capabilities.
def delete():
    #provides for deletion of songs
    db(db.music.id==request.args(0)).delete()
    redirect(URL(r=request, f="view"))
		# The admin has got extra rights and exclusive access to special features not availabe to the common end user.
	     	# 1. Users List
	      	# 2. List of Reported Songs.


@auth.requires_membership('Admin') 
#allows the admin to delete other users at his/her discretion. 
def delete_user(): 
    #the delete user function.   
    db(db.auth_user.id==request.args(0)).delete()
    redirect(URL(r=request, f="users"))
		#the admin may be required to delete a user because of illicit activities or excessive misuse of the facilities provided.

@auth.requires_login()  
#shows the list of registered users to the current user(with admin privileges) logged in.	
def users(): 
    users=db().select(db.auth_user.ALL, orderby=db.auth_user.id)
    return dict(users=users)
	#the above fuction returns a comprehensive list of users to the admin who has logged in.
	#this ensures transparency and prevents anonymous users from availing of the facility.	
 

@auth.requires_login()
def view():
    #function to view all the songs in the  database
    musics=db().select(db.music.ALL, orderby=db.music.name)
    return dict(musics=musics)
	#the above function gives a comprehensive list of all the songs in the music database.	    
	#this allows the user to have a view of the entire database at once.
	#eases navigation of songs and allows for downloading and sampling of good content all at once.		



def search():    
    #function to search songs 
    name=TD('Search music name:') 
    #asks for name of song title
    namebox=TD(INPUT(_id='music_name',_name='music[name]',_size='30',_type='text',requires=IS_NOT_EMPTY()),DIV(_class='auto_complete',_id='music_name_auto_complete'))   
    submit=TD(INPUT(_type='submit',_name='submit',_value='Submit'))

    form=FORM(TABLE(TR(name,namebox,submit)))

    musics=None

    if form.accepts(request.vars,session): 
        search=request.vars['music[name]'] 
        #searches for the requested song amongst those in the database
        musics=db(db.music.name.upper().like('%'+search.upper()+'%')).select(db.music.ALL)
    

    return dict(form=form,musics=musics)
    #returns a list of favourable matches from the collection.

@auth.requires_login()
def user_set():
    return dict()

@auth.requires_login()	
def comment():
    db.comment.user.default = auth.user.id
    #db.comment.user.default = db.comment.user.writable = False
    t=request.args(0)
    form  = SQLFORM(db.comment)
    if form.accepts(request.vars):
		response.flash= 'comment added'
		redirect(URL(r=request, f="comment"))
    return dict(form=form)
	#allows the user to comment on a particular song.
	#flashes "comment added" prompt when a comment is added successfully.


@auth.requires_login()
def view_comment():
    #function to view all the comments made on all songs in the  database
    musics=db().select(db.music.ALL, orderby=db.music.id)
    users=db().select(db.auth_user.ALL, orderby=db.auth_user.id)
    comments=db().select(db.comment.ALL, orderby=db.comment.comment)
    return dict(comments=comments,musics=musics,users=users)
	#returns a title wise description of comments made by all users.
   
@auth.requires_login()
def playlist():
    #function to show playlist of the user who has logged in.
    music=db().select(db.music.ALL, orderby=db.music.id)
    playlist=db().select(db.playlist.ALL, orderby=db.playlist.User_id)
    db.playlist.User_id.default = auth.user.id
    #db.playlist.User_id.default = db.playlist.User_id.writable = False
    t=request.args(0)
    form  = SQLFORM(db.playlist)
    if form.accepts(request.vars):
		response.flash= 'Song added'
                #flashes 'song added' prompt when a particular song is successfully added to the user's playlist.
		redirect(URL(r=request, f="playlist"))
    return dict(form=form,playlist=playlist,music=music)
	#above function allows addition of songs to a playlist.	
	#ensures smooth customisation of the playlist for the current user.

@auth.requires_login()
def view_playlist():
    #function to view all the songs in the playlist of the particular user.
    comments=db().select(db.playlist.ALL, orderby=db.playlist.Song)
    return dict(comments=comments)

@auth.requires_login()
def abuse():
    #allows a user to report abuse, either in form of obscene lyrics or explicit content.
    db.abuse.User.default = auth.user.id
    #db.abuse.User.default = db.abuse.User.writable = False
    t=request.args(0)
    form  = SQLFORM(db.abuse)
    #registers the song in .abuse database which can be later referred.
    if form.accepts(request.vars):
		response.flash= 'reported abuse' 
                #flashes a 'reported abuse' prompt on successful submission of abuse report.
		redirect(URL(r=request, f="navigate"))
    return dict(form=form)
    #the above function directs a list of reported songs to the admin which can be later viewed when a person is logged in as administrator.	

@auth.requires_login()	
def forum():
    users=db().select(db.auth_user.ALL, orderby=db.auth_user.id)
    comments=db().select(db.forum.ALL, orderby=db.forum.Comment)
    db.forum.Users.default = auth.user.id
    #db.forum.Users.default = db.forum.Users.writable = False
    t=request.args(0)
    form  = SQLFORM(db.forum)
    if form.accepts(request.vars):
		response.flash= 'comment added' 
                #flashes 'comment added' prompt on successful posting of query in forum.
		redirect(URL(r=request, f="forum"))
    return dict(form=form, comments=comments,users=users)
    #the above function allows for the creation of a forum where users with similar concerns and questions can ask the admin.
    #here the users can also discuss amongst themselves and suggest improvements to the website or the quality of content added.
    #the forum is a great addition to the already existing options for open criticism.

@auth.requires_login()	
def profile():
    users=db(request.args(0)==db.auth_user.id).select(db.auth_user.ALL)
    pics=db().select(db.picture.ALL, orderby=db.picture.use)
    #musics=db().select(db.music.ALL, orderby=db.music.name)
    return dict(users=users,pics=pics)
    """the function above shows the profile of the users who are there in the database """
