# напиши здесь код создания и управления картой
class Mapmanager():
    """ Управление картой """
    def __init__(self):
        self.model = 'block' # модель кубика лежит в файле block.egg
        # # используются следующие текстуры: 
        self.texture = 'block.png'          
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ] #rgba
        # создаём основной узел карты:
        self.startNew() 
        # self.addBlock((0,10, 0))

    def startNew(self):
        """создаёт основу для новой карты""" 
        self.land = render.attachNewNode("Land") # узел, к которому привязаны все блоки карты

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def addBlock(self, position):
        # создаём строительные блоки 
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture)) 
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)

    def clear(self):
        """обнуляет карту"""
        self.land.removeNode()
        self.startNew()
    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] +1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    



    def loadLand(self, filename):
        """создаёт карту земли из текстового файла, возвращает её размеры"""
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x,y
    

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at="+str(pos))
    def isEmptyc(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z +=1
        return(x, y, z)

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)


    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for i in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)
