import pygame 
import os 


pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode(( WIDTH, HEIGHT ))
pygame.display.set_caption('Space Game')
BORDER = pygame.Rect( 438, 0, 6, HEIGHT)

HEALTH_FONT = pygame.font.SysFont( 'comicsans', 40)
WINNER_FONT = pygame.font.SysFont( 'comicsans', 60 )

FPS = 60
VEL = 3
BULLET_VEL = 35
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1 
RED_HIT = pygame.USEREVENT + 2 

YELLOWSPACESHIP_IMG = pygame.image.load(
    os.path.join('/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets', '/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets/spaceship_yellow.png')
)
YELLOWSPACESHIP = pygame.transform.rotate(pygame.transform.scale( YELLOWSPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT) ), 90)    

REDSPACESHIP_IMG = pygame.image.load(
    os.path.join('/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets', '/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets/spaceship_red.png')
)
REDSPACESHIP = pygame.transform.rotate(pygame.transform.scale( REDSPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT) ), -90) 

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets', '/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets/space.png')), (WIDTH, HEIGHT)
) 

BULLET_HIT_SOUND = pygame.mixer.Sound( os.path.join('/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets', '/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets/Assets_Grenade+1.mp3') )
BULLET_FIRE_SOUND = pygame.mixer.Sound( os.path.join('/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets', '/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets/Assets_Gun+Silencer.mp3'))
BACKGROUND_SOUND = pygame.mixer.Sound( os.path.join('/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets', '/Users/vadim/Documents/Programming/Python/Games/SpaceGame/Assets/Mortal Kombat.mp3') )
BACKGROUND_SOUND.play(-1)


def drawObjects( red, yellow, yellow_bullets, red_bullets, red_health, yellow_health ):

    WIN.blit( SPACE, (0, 0) )
    WIN.blit( YELLOWSPACESHIP, ( yellow.x, yellow.y ) )
    WIN.blit( REDSPACESHIP, ( red.x, red.y ) )
    pygame.draw.rect( WIN, (0, 0, 0), BORDER )
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, (255, 255, 255))
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, (255, 255, 255))
    WIN.blit(red_health_text, ( 20, 20 ))
    WIN.blit(yellow_health_text, ( 685, 20 ))


    for bullet in red_bullets:
        pygame.draw.rect( WIN, (255, 0, 0), bullet )
    
    for bullet in yellow_bullets:
        pygame.draw.rect( WIN, (255, 255, 0), bullet )


    pygame.display.update()

def moveYellowSpaceShip( keys_pressed, yellow ):
    
    if keys_pressed[pygame.K_a] and yellow.x > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x < (BORDER.x - 40): # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y >0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y < 440: # DOWN
        yellow.y += VEL

def moveRedSpaceShip( keys_pressed,red ):
    
    if keys_pressed[pygame.K_LEFT] and red.x > (BORDER.x + 8): # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x < 861: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y < 440: # DOWN
        red.y += VEL

def handle_bullets( yellow_bullets, red_bullets, yellow, red ):
    
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        
        if bullet.x < 0:
            red_bullets.remove(bullet)

def create_winner( text ):

    draw_text = WINNER_FONT.render( text, 1, (255, 255, 255) )
    WIN.blit( draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2)  )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect( 700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT )
    yellow = pygame.Rect( 100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT )

    yellow_bullets = []
    red_bullets = []
    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True 
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                yellow_health -= 1 
                BULLET_HIT_SOUND.play()     

        winner_text = ''

        if red_health <= 0:
            winner_text = 'Red Won the game!!!'

        if yellow_health <= 0:
            winner_text = 'Yellow Won the game!!!'    

        if winner_text != '':
            red_health = 10
            yellow_health = 10
            create_winner(winner_text)



        keys_pressed = pygame.key.get_pressed()

        handle_bullets( yellow_bullets, red_bullets, yellow, red )
        moveYellowSpaceShip( keys_pressed, yellow )
        moveRedSpaceShip( keys_pressed,red )
        drawObjects( red, yellow, yellow_bullets, red_bullets, red_health, yellow_health )
    
    pygame.quit()
    pygame.event.pump()


if __name__ == '__main__':

    main()
            