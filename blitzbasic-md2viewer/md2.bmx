Type TMD2Header
    Field magic : Int
    Field version : Int
    Field skinWidth : Int
    Field skinHeight : Int
    Field frameSize : Int
    Field numSkins : Int
    Field numVertices : Int
    Field numTexCoords : Int
    Field numTriangles : Int
    Field numGlCommands : Int
    Field numFrames : Int
    Field offsetSkins: Int
    Field offsetTexCoords :Int
    Field offsetTriangles : Int
    Field offsetFrames : Int
    Field offsetGlCommands :Int
	Field offsetEnd : Int

	Method LoadFromStream(stream : TStream)
		magic = ReadInt(stream)
		version = ReadInt(stream)
		skinWidth = ReadInt(stream)
		skinHeight = ReadInt(stream)
		frameSize = ReadInt(stream)
		numSkins = ReadInt(stream)
		numVertices = ReadInt(stream)
		numTexCoords = ReadInt(stream)
		numTriangles = ReadInt(stream)
		numGlCommands = ReadInt(stream)
		numFrames = ReadInt(stream)
		offsetSkins = ReadInt(stream)
		offsetTexCoords = ReadInt(stream)
		offsetTriangles = ReadInt(stream)
		offsetFrames = ReadInt(stream)
		offsetGlCommands = ReadInt(stream)
		offsetEnd = ReadInt(stream)	
	End Method
End Type


Type TMD2TriangleVertex

	Field vertex : Byte[3]
	Field lightNormalVertex : Byte
	
	Method LoadFromStream(stream : TStream)
		Local i : Int
		For i = 0 To 2
			vertex[i] = ReadByte(stream)
		Next
		lightNormalVertex = ReadByte(stream)
	End Method
	
	
End Type

Type TMD2Vertex
	Field x : Float
	Field y : Float
	Field z : Float
	
	Method Interpolate : TMD2Vertex(v : TMD2Vertex, factor : Double)
		Local novo : TMD2Vertex
		novo = New TMD2Vertex
		
		novo.x = x + factor * (v.x - x)
		novo.y = y + factor * (v.y - y)
		novo.z = z + factor * (v.z - z)
		
		Return novo
		
	End Method
End Type

Type TMD2Frame

	Field scale : Float[3]
	Field translate : Float[3]
	Field name : String
	Field vertices : TList
	Field calcVert : TList
	
	
	Function Create : TMD2Frame()
		Local novo : TMD2Frame
		novo = New TMD2Frame
		novo.vertices = New TList
		novo.calcVert = New TList
		Return novo
	End Function
	
	Method LoadFromStream(stream : TStream, header : TMD2Header)
		Local i : Int
		
'		SeekStream(stream, header.offsetFrames)
		
		For i = 0 To 2
			scale[i] = ReadFloat(stream)
		Next
		For i = 0 To 2
			translate[i] = ReadFloat(stream)
		Next
		
		name = ReadString(stream, 16)
		
		
		For i = 1 To header.numVertices
			Local triang : TMD2TriangleVertex
			Local cv : TMD2Vertex
			
			
			triang = New TMD2TriangleVertex
			triang.LoadFromStream(stream)
			
			cv = New TMD2Vertex

			cv.x = Float(triang.vertex[0]) * scale[0] + translate[0]
			cv.y = Float(triang.vertex[1]) * scale[1] + translate[1]
			cv.z = Float(triang.vertex[2]) * scale[2] + translate[2]

			calcVert.AddLast cv
			vertices.AddLast triang
		Next
		
	End Method
	
	Method GetVertexAtIndex : TMD2Vertex (vertexIndex : Int)
'		Local novo : TMD2Vertex
'		Local tv : TMD2TriangleVertex
		
'		tv = TMD2TriangleVertex(vertices.ValueAtIndex(vertexIndex))
'		novo = New TMD2Vertex
		
'		novo.x = Float(tv.vertex[0]) * scale[0] + translate[0]
'		novo.y = Float(tv.vertex[1]) * scale[1] + translate[1]
'		novo.z = Float(tv.vertex[2]) * scale[2] + translate[2]
		
'		Return novo
		Return TMD2Vertex(calcVert.ValueAtIndex(vertexIndex))		
	End Method
	
	
	Method PokeVertexData(bank : TBank, address : Int, vertexIndex : Int)
		Local v : Float
		Local i : Int
		Local vertexTriangle  : TMD2TriangleVertex = TMD2TriangleVertex(vertices.ValueAtIndex(vertexIndex))
		
		For i = 0 To 2
			v = Float(vertexTriangle.vertex[i]) * scale[i]
			v :+ translate[i]
			bank.PokeFloat address + i * 4, v 
		Next
		
	End Method
	
	
	Method PokeVerticesData(bank : TBank, address : Int)
		Local i : Int
		For i = 0 To vertices.Count() - 1
			PokeVertexData bank, address + i * 12, i
		Next
	End Method
	
	Method CreateVertexBank : TBank()
		Local bank : TBank
		
		bank = CreateBank(vertices.Count() * 12)
		
		PokeVerticesData bank, 0
		
		Return bank
		
	End Method
	
End Type


Type TMD2Triangle
	Field vertexIndices : Short[3]
	Field textureIndices : Short[3]

	Method LoadFromStream(stream : TStream)
		Local i : Int
		For i = 0 To 2
			vertexIndices[i] = ReadShort(stream)
		Next
		For i = 0 To 2
			textureIndices[i] = ReadShort(stream)
		Next
		
	End Method
	
	
End Type

Type TMD2TriangleList

	Field list : TList
	
	Function Create : TMD2TriangleList()
		Local novo : TMD2TriangleList
		novo = New TMD2TriangleList
		novo.list = New TList
		
		Return novo
	End Function
	
	Method LoadFromStream(stream : TStream, header : TMD2Header)
		Local i : Int
		
		SeekStream(stream, header.offsetTriangles)
		
		For i = 1 To header.numTriangles
			Local triang : TMD2Triangle
			triang  = New TMD2Triangle
			triang.LoadFromStream(stream)
			list.AddLast(triang)
		Next
	
	End Method
End Type

Type TMD2TexCoord
	Field s : Short
	Field t : Short
	
	Method LoadFromStream(stream : TStream)
		s = ReadShort(stream)
		t = ReadShort(stream)	
	End Method	
	
End Type

Type TMD2TCList
	Field list : TList
	
	Field skinWidth : Int
	Field skinHeight : Int
	
	Function Create : TMD2TCList()
		Local novo : TMD2TCList = New TMD2TCList
		novo.list = New TList
		Return novo
	End Function
	
	Method LoadFromStream(stream : TStream, header : TMD2Header)
		SeekStream(stream, header.offsetTexCoords)
		
		skinWidth = header.skinWidth
		skinHeight = header.skinHeight
		
		For i = 1 To header.numVertices
			Local texCoord : TMD2TexCoord = New TMD2TexCoord
			
			texCoord.LoadFromStream(stream)
			list.AddLast(texCoord)
		Next
	
	End Method
	
	Method PokeTexCoord(bank : TBank, address : Int, index : Int)
		Local u : Float
		Local v : Float
		
		Local tc : TMD2TexCoord
		tc = TMD2TexCoord(list.ValueAtIndex(index))
	
		u = Float(tc.s) / Float(skinWidth)
		v = Float(tc.t) / Float(skinHeight)
		
		bank.PokeFloat address, u
		bank.PokeFloat address + 4, v
	
	End Method
	
	Method PokeAllTexCoords(bank : TBank, address : Int)
		Local i : Int
		
		For i = 0 To list.Count() - 1
			PokeTexCoord bank, address, i
		Next
	
	End Method
	
	Method CreateTexCoordBank : TBank()
		Local bank : TBank = CreateBank(list.Count() * 8)
		
		PokeAllTexCoords bank, 0
		
		Return bank
	
	End Method
	
End Type

Type TMD2GLCommandData
	Field s : Float
	Field t : Float
	Field vertexIndex : Int
	
	Method LoadFromStream(stream : TStream)
		s = ReadFloat(stream)
		t = ReadFloat(stream)
		vertexIndex = ReadInt(stream)
	End Method
End Type

Type TMD2GLCommands
	Field numCom : Int
	Field listCom : TList
	
	Function Create : TMD2GLCommands()
		Local novo : TMD2GLCommands = New TMD2GLCommands
		novo.listCom = New TList
		Return novo
	End Function
	
	Method LoadFromStream(stream : TStream)
	
		numCom = ReadInt(stream)
		If numCom <> 0 Then
			For i = 1 To Abs(numCom)
				Local t : TMD2GLCommandData
			
				t = New TMD2GLCommandData
				t.LoadFromStream(stream)
				listCom.AddLast(t)
			
			Next
		End If
	End Method
End Type

Type TMD2GLComList
	Field comList : TList
	
	Function Create : TMD2GLComList()
		Local novo : TMD2GLComList = New TMD2GLComList
		novo.comList = New TList
		Return novo
	End Function
	
	Method LoadFromStream(stream : TStream, header : TMD2Header)
		SeekStream(stream, header.offsetGlCommands)
		
		For i = 1 To header.numGlCommands
			Local md2cs : TMD2GLCommands = TMD2GLCommands.Create()
			md2cs.LoadFromStream(stream)
			If md2cs.numCom <> 0 Then
				comList.AddLast md2cs
			Else
				Exit
			End If
		Next
		
	End Method
		
End Type

Type TMD2

	Field header : TMD2Header
	
	Field frameList : TList
	
	Field triangleList : TMD2TriangleList

	Field texCoordList : TMD2TCList
	
	Field glComList : TMD2GLComList

	Field fileName : String
	
	Field skinGLName : Int
	
	Field hasTexture : Int

	Field isPreparedDE : Int
	
	Field vertexBuffer : TBank
	
	Field ibTriangleFan : TBank

	Field ibTriangleStrip : TBank
		
	Field texCoordBuffer : TBank

	Function Create : TMD2()
		Local novo : TMD2 = New TMD2
		novo.frameList = New TList
		novo.triangleList = TMD2TriangleList.Create()
		novo.texCoordList = TMD2TCList.Create()
		novo.glComList = TMD2GLComList.Create()
		novo.isPreparedDE = 0
		novo.header = New TMD2Header		
		hasTexture = 0
		Return novo
	End Function

	Method LoadFromFile(nome : String, textura : String)
		Local stream : TStream = OpenStream(nome,True,False)
		Local pixm : TPixmap
		
		If Len(textura) > 0 Then
			pixm = LoadPixmap(textura)
			skinGLName = GLTexFromPixmap(pixm)
			hasTexture = 1
		Else
			hasTexture = 0
		End If
		
		header.LoadFromStream stream
		SeekStream(stream, header.offsetFrames)
		For i = 1 To header.numFrames
			Local frame : TMD2Frame
			frame = TMD2Frame.Create()
			frame.LoadFromStream(stream, header)
			frameList.AddLast frame
		Next
		triangleList.LoadFromStream(stream, header)
		texCoordList.LoadFromStream(stream, header)
		glComList.LoadFromStream(stream, header)
		CloseStream(stream)
				
		
	End Method

	Method Draw(frameIndex : Int, interLevel : Double, canBindTexture : Int = 1)
		' Será usado o método de glCommands...
		Local glc : TMD2GLCommands
		Local fra1 : TMD2Frame, fra2 : TMD2Frame
		fra1 = TMD2Frame(frameList.ValueAtIndex(frameIndex))
		fra2 = TMD2Frame(frameList.ValueAtIndex((frameIndex + 1) Mod header.numFrames))
		If hasTexture = 1 And canBindTexture = 1 Then glBindTexture GL_TEXTURE_2D, skinGLName
		
		For glc = EachIn glComList.comList
			Local numVert : Int = glc.numCom
			Local tipoTriang : Int = -1
			If numVert > 0 Then
				tipoTriang = GL_TRIANGLE_STRIP
			ElseIf numvert < 0 Then
				tipoTriang = GL_TRIANGLE_FAN								
			End If
			
			If tipoTriang <> -1 Then
				Local comando : TMD2GLCommandData
				glBegin tipoTriang
				For comando = EachIn glc.listCom
					Local v1 : TMD2Vertex, v2 : TMD2Vertex, v : TMD2Vertex			
					
					v1 = fra1.GetVertexAtIndex(comando.vertexIndex)
					v2 = fra2.GetVertexAtIndex(comando.vertexIndex)

					v = v1.Interpolate(v2, interLevel)

					If hasTexture = 1 And canBindTexture = 1 Then glTexCoord2f comando.s, comando.t									
					glVertex3f v.x, v.y, v.z
'					glVertex3f v1.x, v1.y, v1.z
				Next
								
				glEnd
			
			End If			
					
		Next
		
	
	End Method
	
	
	Method CreateDisplayList : Int()
		Local first : Int
		Local i : Int
		Local j : Int
		first = glGenLists(header.numFrames)
		
		For i=0 To header.numFrames-1
			j = i + first
			glNewList(j, GL_COMPILE)
			Draw(i, 0.0, 0)
			glEndList
		Next
		Return first
	End Method
	
	Method PrepareDrawElements()
		If isPreparedDE = 0 Then
			Local fra1 : TMD2Frame
			Local i : Int
			Local addr : Int
			
			vertexBuffer = CreateBank(header.numFrames * header.numVertices * 12)
			texCoordBuffer = CreateBank(header.numVertices * 8)
			
			addr = 0
			For fra1 = EachIn frameList
				Local v : TMD2Vertex
				
				For v = EachIn fra1.calcVert
					PokeFloat(vertexBuffer, addr, v.x)
					PokeFloat(vertexBuffer, addr + 4, v.y)
					PokeFloat(vertexBuffer, addr + 8, v.z)
					addr :+ 12	
				Next			
			Next
			isPreparedDE = 1
		End If
	End Method
	
	' Este método usa DrawElements...
	Method DrawElements(frameIndex : Int)
		Local i : Int, j : Int
		Local addr : Byte Ptr
		Local comandos : TMD2GLCommands
		Local com : TMD2GLCommandData

		addr = LockBank(vertexBuffer)
		i = Int(addr) + frameIndex * header.numVertices * 12

		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointer(3,GL_FLOAT,0,Byte Ptr(i))
		j = header.numVertices		
		For i = 0 To j - 1
			PokeFloat texCoordBuffer, i * 8, 0.0
			PokeFloat texCoordBuffer, i * 8 + 4, 0.0
		Next
		
		
		Local maxCom : Int
		maxCom = -1
		
		' First, prepare the texCoordBuffer
		
		For comandos = EachIn glComList.comList
			
			If Abs(comandos.numCom) > maxCom Then
				maxCom = Abs(comandos.numCom)
			End If
		'	For com = EachIn comandos.listCom				
		'		PokeFloat texCoordBuffer, com.vertexIndex  * 8, com.s
		'		PokeFloat texCoordBuffer, com.vertexIndex  * 8 + 4, com.t
		'	Next
		Next
		
		' Fine, now lock and load
'		glEnableClientState(GL_TEXTURE_COORD_ARRAY)		
'		glTexCoordPointer(2,GL_FLOAT,0,LockBank(texCoordBuffer))
				
		Local buf : TBank
		buf = CreateBank(maxCom * 4)
		' Now, it's time to draw...
		For comandos = EachIn glComList.comList
			Local nv : Int
			Local modo : Int
			nv = Abs(comandos.numCom)
			If nv = comandos.numCom Then 
				modo = GL_TRIANGLE_STRIP
			Else
				modo = GL_TRIANGLE_FAN
			End If
			'ResizeBank(buf, nv * 4)
			i = 0
			For com = EachIn comandos.listCom				
				PokeInt buf, i * 4, com.vertexIndex
				PokeFloat texCoordBuffer, com.vertexIndex * 8, com.s
				PokeFloat texCoordBuffer, com.vertexIndex * 8 + 4, com.t
				i :+ 1
			Next
			
			glEnableClientState(GL_TEXTURE_COORD_ARRAY)
			glTexCoordPointer(2,GL_FLOAT,0,LockBank(texCoordBuffer))
			glDrawElements(modo,nv,GL_UNSIGNED_INT,LockBank(buf))			
			glDisableClientState(GL_TEXTURE_COORD_ARRAY)
			UnlockBank(texCoordBuffer)
			UnlockBank(buf)
		Next
		
		
		glDisableClientState(GL_VERTEX_ARRAY)
		UnlockBank(vertexBuffer)
	End Method
End Type