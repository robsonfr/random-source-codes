Local width : Int, height : Int
width = 1280
height = 720
Include "md2.bmx"
GLGraphics width,height

Function Set3DViewport(w,h)

	Local aspect#
	

	Local top#, bottom#, lef#, rig#

	If w = 0 Then h = 1

	glViewport 0,0,w,h

	glMatrixMode GL_PROJECTION
	glLoadIdentity
	aspect#=Float(w)/Float(h)
	
	top# = Tan(30) * 1.0
	bottom# = -top#
	lef# = bottom# * aspect#
	rig# = top# * aspect#
	
	
	glFrustum  lef#, rig#, bottom#, top#, 1.0, 100.0
	glMatrixMode GL_MODELVIEW 
	
End Function


Function LoadMD2(fileName)


End Function

	Local p : TPixmap
	Local m : TMD2
	Local offX#, offY#, offZ#
	Local mx%, my%
	Local mov%
	Local indice : Int
	Local md2Arq : String, textura : String
	
	md2Arq = RequestFile("MD2 File")
	textura = RequestFile("Texture")
	
	m = TMD2.Create()
'	m.LoadFromFile("awolf.md2", "awolf.png") 
'	m.LoadFromFile("starfox.md2", "starfox.png")

	m.LoadFromFile(md2Arq,textura)
	Print m.header.numFrames
	Print m.header.numTriangles
	
	'indice = m.CreateDisplayList()
	
	
	'p = LoadPixmap("d:\starfox.png")


	offX# = 0.0
	offY# = 0.0
	offZ# = 0.0

	'tname = GLTexFromPixmap(p)

'	glEnable(GL_BLEND)
'	glBlendFunc(GL_SRC_ALPHA, GL_ONE)
	glEnable(GL_TEXTURE_2D)
	glClearColor(0.65, 0.65, 0.91, 0.0)
	glEnable(GL_DEPTH_TEST)
	
	glEnable GL_AUTO_NORMAL
	glEnable GL_NORMALIZE

	glClearDepth(1.0)
	glDepthFunc(GL_LEQUAL)

	Set3DViewport width,height

	rot = 0.0
	frame = 0
	
	subframe = 0
	
	numsubframes = 2
	
	t2 = 0
	Local fps : Float[5]
	
	i = 0
	
	soma# = 0
	
	num# = 0
	
	Local k : Int
	
	If Len(textura) > 0 Then glBindTexture(GL_TEXTURE_2D, m.skinGLName)
	
	mov% = 0

	m.PrepareDrawElements	
While Not KeyHit(KEY_ESCAPE) And Not AppTerminate()
	t1 = MilliSecs()
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	glMatrixMode GL_MODELVIEW
	glLoadIdentity

	If MouseDown(1) And mov% = 0 Then
		mov% = 1
		mx% = MouseX()
		my% = MouseY()
	Else If Not MouseDown(1) Then
		mov% = 0
	End If
	
	If mov% = 1 Then
		offX# = (MouseX() - mx%) * 40.0 / Double(width)
		offY# = (my% - MouseY()) * 40.0 / Double(height)
		'Print offX# + " " + offY#
	End If

	glTranslatef offX#,offY#,-80.0
'	glRotatef rot,0.0,1.0,0.0	
	glRotatef 270.0,1.0,0.0,0.0
	glRotatef 270.0,0.0,0.0,1.0


	
	
	k = indice + frame
	
'	glCallList(k)
	
'	m.Draw frame, Double(subframe) / Double(numsubframes)
	'm.Draw frame, 0
	m.DrawElements frame
	
'	m.Draw frame, 0
'	glLoadIdentity
'	glTranslatef 0.0,0.0,-60.0

'	glRotatef rot,0.0,1.0,0.0	
'	glRotatef -90.0,1.0,0.0,0.0
'	glRotatef -90.0,0.0,0.0,1.0


	
'	m.Draw frame, Double(subframe) / Double(numsubframes)

'	glLoadIdentity
'	glTranslatef 40.0,0.0,-80.0

'	glRotatef rot,0.0,1.0,0.0	
'	glRotatef -90.0,1.0,0.0,0.0
'	glRotatef -90.0,0.0,0.0,1.0


	
'	m.Draw frame, Double(subframe) / Double(numsubframes)


'	glLoadIdentity
'	glTranslatef -40.0,-40.0,-80.0

'	glRotatef rot,0.0,1.0,0.0	
'	glRotatef -90.0,1.0,0.0,0.0
'	glRotatef -90.0,0.0,0.0,1.0


	
'	m.Draw frame, Double(subframe) / Double(numsubframes)


'	glLoadIdentity
'	glTranslatef 0.0,-40.0,-80.0

'	glRotatef rot,0.0,1.0,0.0	
'	glRotatef -90.0,1.0,0.0,0.0
'	glRotatef -90.0,0.0,0.0,1.0


	
'	m.Draw frame, Double(subframe) / Double(numsubframes)

'	glLoadIdentity
'	glTranslatef 40.0,0.0,-80.0

'	glRotatef rot,0.0,1.0,0.0	
'	glRotatef -90.0,1.0,0.0,0.0
'	glRotatef -90.0,0.0,0.0,1.0


	
'	m.Draw frame, Double(subframe) / Double(numsubframes)


'	glLoadIdentity
'	glTranslatef 40.0,-40.0,-80.0

'	glRotatef rot,0.0,1.0,0.0	
'	glRotatef -90.0,1.0,0.0,0.0
'	glRotatef -90.0,0.0,0.0,1.0


	
'	m.Draw frame, Double(subframe) / Double(numsubframes)


'	glLoadIdentity
'	glTranslatef 40.0,40.0,-80.0

'	glRotatef rot,0.0,1.0,0.0	
'	glRotatef -90.0,1.0,0.0,0.0
'	glRotatef -90.0,0.0,0.0,1.0


	
'	m.Draw frame, Double(subframe) / Double(numsubframes)


'	glLoadIdentity
'	glTranslatef 0.0,40.0,-80.0

'	glRotatef rot,0.0,1.0,0.0	
'	glRotatef -90.0,1.0,0.0,0.0
'	glRotatef -90.0,0.0,0.0,1.0


'	m.Draw frame, Double(subframe) / Double(numsubframes)


'	glLoadIdentity
'	glTranslatef -40.0,40.0,-80.0

'	glRotatef rot,0.0,1.0,0.0	
'	glRotatef -90.0,1.0,0.0,0.0
'	glRotatef -90.0,0.0,0.0,1.0


	

	
'	m.Draw frame, Double(subframe) / Double(numsubframes)
      't2 = (MilliSecs() - t1)
	'If t2 <> 0 Then 
'		fps[i] = 1000.0 / Float(t2) 
'	Else 
'		fps[i] = 0.0
'	End If
	
'	soma# :+ fps[i]
'	num# :+ 1
	
'	i = (i + 1) Mod 5
'	For j = 0 To 4
'		GLDrawText fps[j] + " fps", 20, 40 + j * 20
'	Next

'	GLDrawText soma# / num# + " fps", 20, 40
'	GLDrawText frame + " ", 20, 40
'	rot  :+ 1
	
	If KeyDown(KEY_SPACE) Then 
		subframe :+ 1
		If subframe = numsubframes + 1 Then
			subframe = 0
			frame = (frame + 1) Mod m.header.numFrames
		End If
	End If
	Flip 1
	
Wend


