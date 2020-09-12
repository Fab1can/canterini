import pygame, random, os, time
import simpleaudio as sa

WINDOW_WIDTH=800
WINDOW_HEIGHT=800

ADD_WIDTH=32
ADD_HEIGHT=32
ADD_X=int(WINDOW_WIDTH/2-ADD_WIDTH/2)
ADD_Y=int(3*WINDOW_WIDTH/4)

MENU_WIDTH=int(WINDOW_WIDTH/4)
MENU_HEIGHT=MENU_WIDTH
MENU_X=WINDOW_WIDTH-MENU_WIDTH
MENU_Y=0

TEMPO_WIDTH=int(MENU_WIDTH*3/5)
TEMPO_HEIGHT=int(TEMPO_WIDTH/2)
TEMPO_X=MENU_X+MENU_WIDTH/2-TEMPO_WIDTH/2
TEMPO_Y=MENU_Y+32

SEL_TEMPO_WIDTH=16
SEL_TEMPO_HEIGHT=16
SEL_TEMPO_X=TEMPO_X+13
SEL_TEMPO_Y=TEMPO_Y+5
SEL_TEMPO_SPAN=20

UI_BTN_ADD=0
UI_FORM_MENU=1
UI_FORM_TEMPO=2
UI_SEL_TEMPO_02=3
UI_SEL_TEMPO_04=4
UI_SEL_TEMPO_06=5
UI_SEL_TEMPO_08=6
UI_SEL_TEMPO_1=7

DEBUG_COLOR=(255,0,0)

GUY_TYPES=1

TEMPOS = ["0.2", "0.4", "0.6", "0.8", "1"]

screen=None

guys=[]
sounds=[]
tempo=4

class GameObject(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width=None, height=None, debug=False, visible=True):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(filename)
        self.image = pygame.transform.scale(self.image, (width or self.rect[2], height or self.rect[3]))
        #screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.debug = debug
        self.visible = visible

    def check_point(self, point): #Check if a point is in rect
        return self.rect[0]+self.rect[2]>=point[0]>=self.rect[0] and self.rect[1]+self.rect[3]>=point[1]>=self.rect[1]

    def draw(self):
        global screen
        if self.visible:
            screen.blit(self.image, self.rect)
        if self.debug:
            pygame.draw.rect(screen,DEBUG_COLOR,self.rect)


class Guy(GameObject):
    def __init__(self, id):
        GameObject.__init__(self, 'guy'+str(id)+'.png', random.randint(0,WINDOW_WIDTH), random.randint(0,WINDOW_HEIGHT))
        self.id=id
        self.pitch=11
        self.step=0

    def play(self):
        sounds[self.id][self.pitch][TEMPOS[tempo]].play()

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('img', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print ('Cannot load image:', fullname)
        raise SystemExit
    return image, image.get_rect()

def add_action():
    guys.append(Guy(0))

# define a main function
def main():
    global screen
    # initialize the pygame module
    pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=512, devicename=None)
    pygame.init()

    for i in range(GUY_TYPES):
        sounds.append([])
        for j in range(12):
            sounds[i].append(dict())
            for k in ["0.2","0.4","0.6","0.8","1"]:
                sounds[i][j][k]=pygame.mixer.Sound(os.path.join('sound',str(i),str(j)+"-"+k+".wav"))

    pygame.display.set_caption("minimal program")

    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

    screen.fill((255,255,255))

    ui = []*10

    ui[UI_BTN_ADD] = GameObject("add.png", ADD_X, ADD_Y, ADD_WIDTH, ADD_HEIGHT)

    ui[UI_FORM_MENU] = GameObject("menu.png", MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT)

    ui[UI_FORM_TEMPO] = GameObject("tempo.png", TEMPO_X, TEMPO_Y, TEMPO_WIDTH, TEMPO_HEIGHT)

    ui[UI_SEL_TEMPO_02] = GameObject("selected.png", SEL_TEMPO_X+0*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=0==tempo)

    ui[UI_SEL_TEMPO_04] = GameObject("selected.png", SEL_TEMPO_X+1*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=1==tempo)

    ui[UI_SEL_TEMPO_06] = GameObject("selected.png", SEL_TEMPO_X+2*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=2==tempo)

    ui[UI_SEL_TEMPO_08] = GameObject("selected.png", SEL_TEMPO_X+3*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=3==tempo)

    ui[UI_SEL_TEMPO_1] = GameObject("selected.png", SEL_TEMPO_X+4*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=4==tempo)

    running = True
    grabbing = False

    step=0
    next=0

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button==1:
                    if grabbing:
                        grabbing = False
                    elif ADD_X+ADD_WIDTH>=event.pos[0]>=ADD_X and ADD_Y+ADD_HEIGHT>=event.pos[1]>=ADD_Y:
                        add_action()
                elif event.button==3:
                    for i in range(len(guys)-1, -1, -1):
                        if guys[i].rect[0]+guys[i].rect[2]>=event.pos[0]>=guys[i].rect[0] and guys[i].rect[1]+guys[i].rect[3]>=event.pos[1]>=guys[i].rect[1]:
                            guys.pop(i)
                            break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    for i in range(len(guys)-1, -1, -1):
                        if guys[i].rect[0]+guys[i].rect[2]>=event.pos[0]>=guys[i].rect[0] and guys[i].rect[1]+guys[i].rect[3]>=event.pos[1]>=guys[i].rect[1]:
                            guys[i], guys[len(guys)-1] = guys[len(guys)-1], guys[i]
                            grabbing = True
                            break
            elif event.type == pygame.MOUSEMOTION:
                if grabbing:
                    guys[len(guys)-1].rect[0]=event.pos[0]-guys[len(guys)-1].rect[2]/2
                    guys[len(guys)-1].rect[1]=event.pos[1]-guys[len(guys)-1].rect[3]/2

        if time.time()>next:
            print(step)
            next=time.time()+float(TEMPOS[tempo])
            for guy in guys:
                if guy.step==step:
                    guy.play()
            step+=1
            step=step%4

        screen.fill((255,255,255))
        for guy in guys:
            guy.draw()
        for obj in ui:
            obj.draw()

        pygame.display.flip()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()