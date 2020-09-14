import pygame, random, os, time
import simpleaudio as sa

WINDOW_WIDTH=800
WINDOW_HEIGHT=800

ADD_WIDTH=32
ADD_HEIGHT=32
ADD_X=WINDOW_WIDTH/2-ADD_WIDTH/2
ADD_Y=3*WINDOW_WIDTH/4

MENU_WIDTH=WINDOW_WIDTH/4
MENU_HEIGHT=1.4*MENU_WIDTH
MENU_X=WINDOW_WIDTH-MENU_WIDTH
MENU_Y=0

TEMPO_WIDTH=MENU_WIDTH*3/5
TEMPO_HEIGHT=TEMPO_WIDTH/2
TEMPO_X=MENU_X+MENU_WIDTH/2-TEMPO_WIDTH/2
TEMPO_Y=MENU_Y+32

SEL_TEMPO_WIDTH=20
SEL_TEMPO_HEIGHT=20
SEL_TEMPO_X=TEMPO_X+10
SEL_TEMPO_Y=TEMPO_Y+15
SEL_TEMPO_SPAN=20

PIANO_X=TEMPO_X-5
PIANO_Y=TEMPO_Y+TEMPO_HEIGHT+15
PIANO_HEIGHT=50
PIANO_WIDTH=140
PIANO_UNSELECTED_SIZE=PIANO_WIDTH/10
PIANO_UNSELECTED_WHITE_Y=PIANO_Y+8*PIANO_HEIGHT/12
PIANO_UNSELECTED_WHITE_X=PIANO_X+((PIANO_WIDTH/7)-PIANO_UNSELECTED_SIZE)/2
PIANO_UNSELECTED_BLACK_Y=PIANO_Y+1*PIANO_HEIGHT/3
PIANO_UNSELECTED_BLACK_X=PIANO_X+(PIANO_WIDTH/11)

STEP_X=MENU_X+15
STEP_Y=PIANO_Y+PIANO_HEIGHT+15
STEP_WIDTH=30
STEP_HEIGHT=30
STEP_SPACING=15

UI_BTN_ADD=0
UI_FORM_MENU=1
UI_FORM_TEMPO=2
UI_SEL_TEMPO_02=3
UI_SEL_TEMPO_04=4
UI_SEL_TEMPO_06=5
UI_SEL_TEMPO_08=6
UI_SEL_TEMPO_1=7
UI_PIANO=8
UI_PIANO_C=9
UI_PIANO_D=10
UI_PIANO_E=11
UI_PIANO_F=12
UI_PIANO_G=13
UI_PIANO_A=14
UI_PIANO_B=15
UI_PIANO_Db=16
UI_PIANO_Eb=17
UI_PIANO_Gb=18
UI_PIANO_Ab=19
UI_PIANO_Bb=20
UI_STEP_1=21
UI_STEP_2=22
UI_STEP_3=23
UI_STEP_4=24
UI_STEP_SEL_1=25
UI_STEP_SEL_2=26
UI_STEP_SEL_3=27
UI_STEP_SEL_4=28

UI_PITCHES = [UI_PIANO_C, UI_PIANO_Db, UI_PIANO_D, UI_PIANO_Eb, UI_PIANO_E, UI_PIANO_F, UI_PIANO_Gb, UI_PIANO_G, UI_PIANO_Ab, UI_PIANO_A, UI_PIANO_Bb, UI_PIANO_B]

DEBUG_COLOR=(255,0,0)

GUY_TYPES=1

TEMPOS = ["0.2", "0.4", "0.6", "0.8", "1"]

screen=None

ui = [None]*29

guys=[]
sounds=[]
tempo=2

def clean_int(num):
    if num==None:
        return None
    else:
        return int(num)

class GameObject(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width=None, height=None, debug=False, visible=True):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(filename)
        self.image = pygame.transform.scale(self.image, (clean_int(width) or self.rect[2], clean_int(height) or self.rect[3]))
        self.area = screen.get_rect()
        self.rect=self.image.get_rect()
        self.rect[0] = int(x)
        self.rect[1] = int(y)
        self.debug = debug
        self.visible = visible

    def check_point(self, point): #Check if a point is in rect
        return self.rect[0]+self.rect[2]>=point[0]>=self.rect[0] and self.rect[1]+self.rect[3]>=point[1]>=self.rect[1]

    def draw(self):
        global screen
        if self.visible:
            screen.blit(self.image, self.rect)
        if self.debug:
            pygame.draw.rect(screen,DEBUG_COLOR,self.rect,True)

    def set_image(self, image):
        self.image = pygame.transform.scale(image, (self.rect[2], self.rect[3]))


class Guy(GameObject):
    def __init__(self, id):
        GameObject.__init__(self, 'guy'+str(id)+'.png', random.randint(0,WINDOW_WIDTH), random.randint(0,WINDOW_HEIGHT))
        self.id=id
        self.pitch=0
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

def change_tempo(new_tempo):
    global tempo
    if tempo!=new_tempo:
        ui[UI_SEL_TEMPO_02+tempo].visible=False
        ui[UI_SEL_TEMPO_02+new_tempo].visible=True
        tempo=new_tempo

def init_ui():
    ui[UI_BTN_ADD] = GameObject("add.png", ADD_X, ADD_Y, ADD_WIDTH, ADD_HEIGHT)

    ui[UI_FORM_MENU] = GameObject("menu.png", MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT)

    ui[UI_FORM_TEMPO] = GameObject("tempo.png", TEMPO_X, TEMPO_Y, TEMPO_WIDTH, TEMPO_HEIGHT)

    seldebug=False

    ui[UI_SEL_TEMPO_02] = GameObject("selected.png", SEL_TEMPO_X+0*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=0==tempo, debug=seldebug)

    ui[UI_SEL_TEMPO_04] = GameObject("selected.png", SEL_TEMPO_X+1*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=1==tempo, debug=seldebug)

    ui[UI_SEL_TEMPO_06] = GameObject("selected.png", SEL_TEMPO_X+2*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=2==tempo, debug=seldebug)

    ui[UI_SEL_TEMPO_08] = GameObject("selected.png", SEL_TEMPO_X+3*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=3==tempo, debug=seldebug)

    ui[UI_SEL_TEMPO_1] = GameObject("selected.png", SEL_TEMPO_X+4*SEL_TEMPO_SPAN, SEL_TEMPO_Y, SEL_TEMPO_WIDTH, SEL_TEMPO_HEIGHT, visible=4==tempo, debug=seldebug)

    ui[UI_PIANO] = GameObject("piano.png", PIANO_X, PIANO_Y, PIANO_WIDTH, PIANO_HEIGHT)

    ui[UI_PIANO_C] = GameObject("unselected.png", PIANO_UNSELECTED_WHITE_X, PIANO_UNSELECTED_WHITE_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_D] = GameObject("unselected.png", PIANO_UNSELECTED_WHITE_X+PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2, PIANO_UNSELECTED_WHITE_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_E] = GameObject("unselected.png", PIANO_UNSELECTED_WHITE_X+(PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2)*2, PIANO_UNSELECTED_WHITE_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_F] = GameObject("unselected.png", PIANO_UNSELECTED_WHITE_X+(PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2)*3, PIANO_UNSELECTED_WHITE_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_G] = GameObject("unselected.png", PIANO_UNSELECTED_WHITE_X+(PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2)*4, PIANO_UNSELECTED_WHITE_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_A] = GameObject("unselected.png", PIANO_UNSELECTED_WHITE_X+(PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2)*5, PIANO_UNSELECTED_WHITE_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_B] = GameObject("unselected.png", PIANO_UNSELECTED_WHITE_X+(PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2)*6, PIANO_UNSELECTED_WHITE_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_Db] = GameObject("unselected.png", PIANO_UNSELECTED_BLACK_X, PIANO_UNSELECTED_BLACK_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_Eb] = GameObject("unselected.png", PIANO_UNSELECTED_BLACK_X+PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2, PIANO_UNSELECTED_BLACK_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_Gb] = GameObject("unselected.png", PIANO_UNSELECTED_BLACK_X+(PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2)*3, PIANO_UNSELECTED_BLACK_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_Ab] = GameObject("unselected.png", PIANO_UNSELECTED_BLACK_X+(PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2)*4, PIANO_UNSELECTED_BLACK_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_PIANO_Bb] = GameObject("unselected.png", PIANO_UNSELECTED_BLACK_X+(PIANO_UNSELECTED_SIZE+((PIANO_WIDTH/14)-(PIANO_UNSELECTED_SIZE/2))*2)*5, PIANO_UNSELECTED_BLACK_Y, PIANO_UNSELECTED_SIZE, PIANO_UNSELECTED_SIZE)

    ui[UI_STEP_1] = GameObject("step1.png", STEP_X, STEP_Y, STEP_WIDTH, STEP_HEIGHT)
    ui[UI_STEP_SEL_1] = GameObject("unselected.png", STEP_X, STEP_Y, STEP_WIDTH, STEP_HEIGHT, visible=False)

    ui[UI_STEP_2] = GameObject("step2.png", STEP_X+STEP_WIDTH+STEP_SPACING, STEP_Y, STEP_WIDTH, STEP_HEIGHT)
    ui[UI_STEP_SEL_2] = GameObject("unselected.png", STEP_X+STEP_WIDTH+STEP_SPACING, STEP_Y, STEP_WIDTH, STEP_HEIGHT, visible=False)

    ui[UI_STEP_3] = GameObject("step3.png", STEP_X+(STEP_WIDTH+STEP_SPACING)*2, STEP_Y, STEP_WIDTH, STEP_HEIGHT)
    ui[UI_STEP_SEL_3] = GameObject("unselected.png", STEP_X+(STEP_WIDTH+STEP_SPACING)*2, STEP_Y, STEP_WIDTH, STEP_HEIGHT, visible=False)

    ui[UI_STEP_4] = GameObject("step4.png", STEP_X+(STEP_WIDTH+STEP_SPACING)*3, STEP_Y, STEP_WIDTH, STEP_HEIGHT)
    ui[UI_STEP_SEL_4] = GameObject("unselected.png", STEP_X+(STEP_WIDTH+STEP_SPACING)*3, STEP_Y, STEP_WIDTH, STEP_HEIGHT, visible=False)

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

    init_ui()

    IMAGE_UNSELECTED = load_png("unselected.png")[0]
    IMAGE_SELECTED = load_png("selected.png")[0]

    running = True
    grabbing = False
    changing_tempo = False

    step=0
    next=0

    selected_note=-1
    selected_step=-1

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
                    elif ui[UI_BTN_ADD].check_point(event.pos):
                        add_action()
                    elif changing_tempo==True:
                        changing_tempo=False
                    else:
                        if selected_note!=-1:
                            for pitch in range(len(UI_PITCHES)):
                                if guys[len(guys)-1].pitch==pitch:
                                    pass
                                elif ui[UI_PITCHES[pitch]].check_point(event.pos):
                                    guys[len(guys)-1].pitch=pitch
                                    ui[UI_PITCHES[selected_note]].set_image(IMAGE_UNSELECTED)
                                    selected_note=pitch
                                    ui[UI_PITCHES[selected_note]].set_image(IMAGE_SELECTED)
                        if selected_step!=-1:
                            for step in range(4):
                                if guys[len(guys)-1].step==step:
                                    pass
                                elif ui[UI_STEP_1+step].check_point(event.pos):
                                    guys[len(guys)-1].step=step
                                    ui[UI_STEP_SEL_1+selected_step].visible=False
                                    selected_step=step
                                    ui[UI_STEP_SEL_1+selected_step].visible=True
                elif event.button==3:
                    if not grabbing:
                        for i in range(len(guys)-1, -1, -1):
                            if guys[i].check_point(event.pos):
                                guys.pop(i)
                                if len(guys)==0:
                                    selected_note=-1
                                    selected_step=-1
                                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if ui[UI_SEL_TEMPO_02+tempo].check_point(event.pos):
                        changing_tempo=True
                    for i in range(len(guys)-1, -1, -1):
                        if guys[i].check_point(event.pos):
                            guys[i], guys[len(guys)-1] = guys[len(guys)-1], guys[i]
                            grabbing = True
                            if guys[len(guys)-1].pitch!=selected_note:
                                ui[UI_PITCHES[selected_note]].set_image(IMAGE_UNSELECTED)
                                selected_note=guys[len(guys)-1].pitch
                                ui[UI_PITCHES[selected_note]].set_image(IMAGE_SELECTED)
                            if guys[len(guys)-1].step!=selected_step:
                                if selected_step!=-1:
                                    ui[UI_STEP_SEL_1+selected_step].visible = False
                                selected_step=guys[len(guys)-1].step
                                ui[UI_STEP_SEL_1+selected_step].visible = True
                            break
            elif event.type == pygame.MOUSEMOTION:
                if grabbing:
                    guys[len(guys)-1].rect[0]=event.pos[0]-guys[len(guys)-1].rect[2]/2
                    guys[len(guys)-1].rect[1]=event.pos[1]-guys[len(guys)-1].rect[3]/2
                elif changing_tempo:
                    for ui_indexes in range(UI_SEL_TEMPO_02, UI_SEL_TEMPO_1+1):
                        if ui_indexes==UI_SEL_TEMPO_02+tempo:
                            pass
                        elif ui[ui_indexes].check_point(event.pos):
                            change_tempo(ui_indexes-UI_SEL_TEMPO_02)

        if time.time()>next:
            #print(step)
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