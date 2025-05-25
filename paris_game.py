import pygame
import sys
import random
import os
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Paris Street Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
LIGHT_BLUE = (135, 206, 235)
LIGHT_GRAY = (200, 200, 200)

# Game states
SCENE_SQUARE = 0
SCENE_DEMO = 1
SCENE_GAME = 2
GAME_OVER = 3

# Game variables
current_scene = SCENE_SQUARE
player_money = 100
selected_cup = None
tourist_cup = None  # Cup selected by the tourist
tourist_position = (700, 300)  # Default position for tourist when not at cup
tourist_at_cup = False  # Whether tourist is standing at their cup
ball_position = 1  # 0, 1, or 2
cups_positions = [(200, 400), (400, 400), (600, 400)]
shuffle_moves = []
current_shuffle_move = 0
shuffle_timer = 0
shuffle_speed = 10  # Slower speed for more visible shuffling
game_state = "intro"  # "intro", "betting", "shuffling", "reveal", "result"
message = "Game starts! Look, the ball is here."
result_timer = 0
cup_animation_offset = 200  # For cup animation
cup_animation_speed = 5
shuffle_visible = True  # Make shuffling visible

# Player character
player_pos = [400, 300]
player_speed = 3
player_direction = 0  # 0: down, 1: left, 2: right, 3: up

# Create directory for assets if it doesn't exist
os.makedirs(os.path.join(os.path.dirname(__file__), 'assets'), exist_ok=True)

# Function to create simple images for the game
def create_simple_images():
    # Create a simple Eiffel Tower image
    eiffel = pygame.Surface((200, 300), pygame.SRCALPHA)
    pygame.draw.polygon(eiffel, BLACK, [(100, 0), (70, 300), (130, 300)])
    pygame.draw.polygon(eiffel, BLACK, [(50, 150), (150, 150), (130, 0), (70, 0)])
    pygame.draw.rect(eiffel, BLACK, (60, 300, 80, 20))
    
    # Create a simple player character (LEGO-like)
    player = pygame.Surface((30, 50), pygame.SRCALPHA)
    # Head
    pygame.draw.circle(player, YELLOW, (15, 10), 10)
    # Body
    pygame.draw.rect(player, BLUE, (5, 20, 20, 20))
    # Legs
    pygame.draw.rect(player, BLACK, (5, 40, 8, 10))
    pygame.draw.rect(player, BLACK, (17, 40, 8, 10))
    
    # Create a simple tourist character
    tourist = pygame.Surface((30, 50), pygame.SRCALPHA)
    # Head
    pygame.draw.circle(tourist, YELLOW, (15, 10), 10)
    # Body
    pygame.draw.rect(tourist, RED, (5, 20, 20, 20))
    # Legs
    pygame.draw.rect(tourist, BLACK, (5, 40, 8, 10))
    pygame.draw.rect(tourist, BLACK, (17, 40, 8, 10))
    
    # Create a simple cup
    cup = pygame.Surface((60, 70), pygame.SRCALPHA)
    pygame.draw.polygon(cup, BLUE, [(5, 60), (55, 60), (45, 10), (15, 10)])
    pygame.draw.ellipse(cup, BLUE, (5, 55, 50, 15))
    
    # Create a simple ball
    ball = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(ball, RED, (15, 15), 15)
    
    # Create a simple arrow
    arrow = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.polygon(arrow, GREEN, [(15, 0), (30, 15), (20, 15), (20, 30), (10, 30), (10, 15), (0, 15)])
    
    # Save the images
    pygame.image.save(eiffel, os.path.join(os.path.dirname(__file__), 'assets', 'eiffel.png'))
    pygame.image.save(player, os.path.join(os.path.dirname(__file__), 'assets', 'player.png'))
    pygame.image.save(tourist, os.path.join(os.path.dirname(__file__), 'assets', 'tourist.png'))
    pygame.image.save(cup, os.path.join(os.path.dirname(__file__), 'assets', 'cup.png'))
    pygame.image.save(ball, os.path.join(os.path.dirname(__file__), 'assets', 'ball.png'))
    pygame.image.save(arrow, os.path.join(os.path.dirname(__file__), 'assets', 'arrow.png'))
    
    # Create a simple background for the square
    square_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    square_bg.fill(LIGHT_BLUE)  # Sky
    pygame.draw.rect(square_bg, GRAY, (0, 400, WINDOW_WIDTH, 200))  # Ground
    pygame.image.save(square_bg, os.path.join(os.path.dirname(__file__), 'assets', 'square_bg.png'))

# Create the simple images
create_simple_images()

# Load images
try:
    eiffel_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'eiffel.png'))
    player_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'player.png'))
    tourist_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'tourist.png'))
    cup_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'cup.png'))
    ball_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'ball.png'))
    arrow_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'arrow.png'))
    square_bg = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'square_bg.png'))
except Exception as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

# Create tourist characters for the square scene
tourists = []
for i in range(15):
    x = random.randint(50, WINDOW_WIDTH - 50)
    y = random.randint(350, 550)
    tourists.append({"pos": (x, y), "moving": random.choice([True, False])})

# Create a group of tourists (the game spot)
game_spot = {"pos": (600, 450), "tourists": []}
for i in range(5):
    angle = i * (2 * math.pi / 5)
    x = game_spot["pos"][0] + int(40 * math.cos(angle))
    y = game_spot["pos"][1] + int(40 * math.sin(angle))
    game_spot["tourists"].append({"pos": (x, y)})

# Font setup
font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 24)

def draw_scene_square():
    """Draw the square scene with Eiffel Tower and tourists"""
    # Draw background
    screen.blit(square_bg, (0, 0))
    
    # Draw Eiffel Tower
    screen.blit(eiffel_img, (300, 100))
    
    # Draw tourists
    for tourist in tourists:
        screen.blit(tourist_img, tourist["pos"])
    
    # Draw the game spot (group of tourists)
    for tourist in game_spot["tourists"]:
        screen.blit(tourist_img, tourist["pos"])
    
    # Draw player
    screen.blit(player_img, player_pos)
    
    # Draw arrow above player
    screen.blit(arrow_img, (player_pos[0], player_pos[1] - 30))
    
    # Draw UI
    pygame.draw.rect(screen, WHITE, (0, 0, WINDOW_WIDTH, 60))
    pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, 60), 2)
    
    money_text = font.render(f"Money: {player_money} €", True, BLACK)
    screen.blit(money_text, (20, 20))
    
    instruction = small_font.render("Use arrow keys to move. Find the street game.", True, BLACK)
    screen.blit(instruction, (WINDOW_WIDTH//2 - instruction.get_width()//2, 20))

def draw_scene_demo():
    """Draw the demonstration scene of the cup game"""
    # Draw background (simple gray)
    screen.fill(LIGHT_GRAY)
    
    # Draw UI area at top
    pygame.draw.rect(screen, WHITE, (0, 0, WINDOW_WIDTH, 60))
    pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, 60), 2)
    
    money_text = font.render(f"Money: {player_money} €", True, BLACK)
    screen.blit(money_text, (20, 20))
    
    # Draw ball in the middle
    screen.blit(ball_img, (400 - ball_img.get_width()//2, 380))
    
    # Draw street vendor (simplified)
    pygame.draw.circle(screen, BLACK, (400, 300), 20)  # Head
    pygame.draw.rect(screen, BROWN, (380, 320, 40, 60))  # Body
    
    # Draw tourist on the right
    pygame.draw.circle(screen, YELLOW, (600, 300), 20)  # Head
    pygame.draw.rect(screen, GREEN, (580, 320, 40, 60))  # Body
    
    # Draw money being bet
    pygame.draw.rect(screen, GREEN, (590, 390, 20, 10))  # Money
    
    # Draw message
    msg = font.render("The street vendor shows the ball and prepares the cups...", True, BLACK)
    screen.blit(msg, (WINDOW_WIDTH//2 - msg.get_width()//2, 500))
    
    # Draw continue instruction
    continue_text = small_font.render("Click to continue", True, BLACK)
    screen.blit(continue_text, (WINDOW_WIDTH//2 - continue_text.get_width()//2, 550))

def generate_shuffle_sequence(num_moves=10):
    """Generate a sequence of cup swaps"""
    global shuffle_moves
    shuffle_moves = []
    positions = [0, 1, 2]
    for _ in range(num_moves):
        # Select two random positions to swap
        i, j = random.sample(positions, 2)
        shuffle_moves.append((i, j))

def perform_shuffle_move(move_index):
    """Perform a single shuffle move"""
    global cups_positions, ball_position
    if move_index < len(shuffle_moves):
        i, j = shuffle_moves[move_index]
        
        # For visual effect, create intermediate positions
        if shuffle_visible:
            # Get original positions
            pos_i = cups_positions[i]
            pos_j = cups_positions[j]
            
            # Draw intermediate positions (raise cups slightly during swap)
            cups_positions[i] = (pos_i[0], pos_i[1] - 20)
            cups_positions[j] = (pos_j[0], pos_j[1] - 20)
            draw_scene_game()
            pygame.display.flip()
            pygame.time.delay(50)
            
            # Move cups horizontally
            cups_positions[i] = (pos_j[0], pos_i[1] - 20)
            cups_positions[j] = (pos_i[0], pos_j[1] - 20)
            draw_scene_game()
            pygame.display.flip()
            pygame.time.delay(50)
            
            # Lower cups to final positions
            cups_positions[i] = pos_j
            cups_positions[j] = pos_i
        else:
            # Just swap positions without animation
            cups_positions[i], cups_positions[j] = cups_positions[j], cups_positions[i]
        
        # Update ball position if needed
        if ball_position == i:
            ball_position = j
        elif ball_position == j:
            ball_position = i

def draw_scene_game():
    """Draw the actual cup game scene"""
    # Draw background (simple gray)
    screen.fill(LIGHT_GRAY)
    
    # Draw UI area at top
    pygame.draw.rect(screen, WHITE, (0, 0, WINDOW_WIDTH, 60))
    pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, 60), 2)
    
    money_text = font.render(f"Money: {player_money} €", True, BLACK)
    screen.blit(money_text, (20, 20))
    
    # Draw street vendor (simplified)
    pygame.draw.circle(screen, BLACK, (400, 300), 20)  # Head
    pygame.draw.rect(screen, BROWN, (380, 320, 40, 60))  # Body
    
    # Draw tourist (simplified) - position depends on game state
    if tourist_at_cup:
        # Tourist standing near their chosen cup
        tourist_x = cups_positions[tourist_cup][0]
        tourist_y = 300
    else:
        # Tourist standing away during shuffling
        tourist_x, tourist_y = tourist_position
    
    pygame.draw.circle(screen, YELLOW, (tourist_x, tourist_y), 20)  # Head
    pygame.draw.rect(screen, GREEN, (tourist_x - 20, tourist_y + 20, 40, 60))  # Body
    
    # Draw cups based on game state
    if game_state == "intro":
        # Show the ball first
        screen.blit(ball_img, (400 - ball_img.get_width()//2, 380))
        
        # Draw cups above their final positions (for animation)
        cup_y_offset = cup_animation_offset
        for i, pos in enumerate(cups_positions):
            screen.blit(cup_img, (pos[0] - cup_img.get_width()//2, pos[1] - cup_img.get_height() - cup_y_offset))
    else:
        # Draw cups in normal positions
        for i, pos in enumerate(cups_positions):
            # Highlight the tourist's cup
            if i == tourist_cup and tourist_at_cup:
                pygame.draw.circle(screen, GREEN, pos, 40, 3)
                
            # Highlight player's selected cup
            is_selected = (selected_cup == i and game_state == "betting")
            if is_selected:
                pygame.draw.circle(screen, YELLOW, pos, 40, 3)
                
            screen.blit(cup_img, (pos[0] - cup_img.get_width()//2, pos[1] - cup_img.get_height()))
        
        # Draw ball if in reveal state
        if game_state == "reveal" or game_state == "result":
            ball_pos = cups_positions[ball_position]
            screen.blit(ball_img, (ball_pos[0] - ball_img.get_width()//2, ball_pos[1] - 20))
    
    # Draw message
    msg_text = font.render(message, True, BLACK)
    screen.blit(msg_text, (WINDOW_WIDTH//2 - msg_text.get_width()//2, 500))
    
    # Draw instructions based on game state
    if game_state == "intro":
        instr = small_font.render("Watch carefully...", True, BLACK)
        screen.blit(instr, (WINDOW_WIDTH//2 - instr.get_width()//2, 550))
    elif game_state == "betting":
        instr = small_font.render("Click on a cup to place your 10€ bet (not the tourist's cup)", True, BLACK)
        screen.blit(instr, (WINDOW_WIDTH//2 - instr.get_width()//2, 550))
    elif game_state == "shuffling":
        instr = small_font.render("The cups are being shuffled...", True, BLACK)
        screen.blit(instr, (WINDOW_WIDTH//2 - instr.get_width()//2, 550))
    elif game_state == "result":
        instr = small_font.render("Click to continue", True, BLACK)
        screen.blit(instr, (WINDOW_WIDTH//2 - instr.get_width()//2, 550))

def draw_game_over():
    """Draw the game over screen"""
    screen.fill(BLACK)
    
    game_over_text = font.render("GAME OVER - You lost all your money!", True, WHITE)
    screen.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, WINDOW_HEIGHT//2 - 50))
    
    restart_text = font.render("Play again? (Y/N)", True, WHITE)
    screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, WINDOW_HEIGHT//2 + 50))

def handle_square_input(event):
    """Handle input for the square scene"""
    global player_pos, current_scene
    
    # Check if player is near the game spot
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 30, 50)
    game_spot_rect = pygame.Rect(game_spot["pos"][0] - 50, game_spot["pos"][1] - 50, 100, 100)
    
    if player_rect.colliderect(game_spot_rect):
        current_scene = SCENE_DEMO

def handle_demo_input(event):
    """Handle input for the demonstration scene"""
    global current_scene
    
    if event.type == MOUSEBUTTONDOWN:
        current_scene = SCENE_GAME
        reset_game()

def reset_game():
    """Reset the game state for a new round"""
    global game_state, selected_cup, tourist_cup, ball_position, message, shuffle_moves, current_shuffle_move, shuffle_timer, cup_animation_offset, tourist_at_cup
    
    game_state = "intro"
    selected_cup = None
    ball_position = random.randint(0, 2)
    
    # Randomly select a cup for the tourist (either leftmost or rightmost)
    tourist_cup = random.choice([0, 2])  # 0 for left, 2 for right
    tourist_at_cup = False  # Tourist starts away from cup
    
    message = "Game starts! Look, the ball is here."
    shuffle_moves = []
    current_shuffle_move = 0
    shuffle_timer = 0
    cup_animation_offset = 200  # Reset cup animation

def handle_game_input(event):
    """Handle input for the game scene"""
    global selected_cup, game_state, player_money, message, result_timer, current_scene
    
    if game_state == "betting" and event.type == MOUSEBUTTONDOWN:
        # Check if a cup was clicked
        for i, cup_pos in enumerate(cups_positions):
            cup_rect = pygame.Rect(cup_pos[0] - 30, cup_pos[1] - 70, 60, 70)
            if cup_rect.collidepoint(event.pos):
                # Can't select the tourist's cup
                if i == tourist_cup:
                    message = "That cup is already chosen by the tourist. Pick another one."
                    return
                    
                selected_cup = i
                game_state = "reveal"
                message = f"You bet 10€ on cup {i+1}."
                return
    
    elif game_state == "result" and event.type == MOUSEBUTTONDOWN:
        # Check if player has any money left
        if player_money <= 0:
            current_scene = GAME_OVER
        else:
            reset_game()
    
    # Skip intro animation with click
    elif game_state == "intro" and event.type == MOUSEBUTTONDOWN:
        game_state = "shuffling"
        message = "The cups are being shuffled! Watch carefully!"
        cup_animation_offset = 0
        # Start shuffling
        generate_shuffle_sequence(15)

def handle_game_over_input(event):
    """Handle input for the game over scene"""
    global current_scene, player_money
    
    if event.type == KEYDOWN:
        if event.key == K_y:
            # Restart the game
            player_money = 100
            current_scene = SCENE_SQUARE
            reset_game()
        elif event.key == K_n:
            pygame.quit()
            sys.exit()

def update_square():
    """Update the square scene"""
    global player_pos, player_direction
    
    # Move player based on key presses
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player_pos[0] -= player_speed
        player_direction = 1
    if keys[K_RIGHT]:
        player_pos[0] += player_speed
        player_direction = 2
    if keys[K_UP]:
        player_pos[1] -= player_speed
        player_direction = 3
    if keys[K_DOWN]:
        player_pos[1] += player_speed
        player_direction = 0
    
    # Keep player within screen bounds
    player_pos[0] = max(0, min(player_pos[0], WINDOW_WIDTH - 30))
    player_pos[1] = max(60, min(player_pos[1], WINDOW_HEIGHT - 50))
    
    # Move some tourists randomly
    for tourist in tourists:
        if tourist["moving"] and random.random() < 0.02:
            x, y = tourist["pos"]
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            tourist["pos"] = (x + dx, y + dy)

def update_game():
    """Update the game scene"""
    global game_state, current_shuffle_move, shuffle_timer, message, player_money, result_timer, ball_position, cup_animation_offset, tourist_at_cup
    
    if game_state == "intro":
        # Animate cups coming down to cover the ball
        cup_animation_offset -= cup_animation_speed
        if cup_animation_offset <= 0:
            cup_animation_offset = 0
            game_state = "shuffling"
            message = "The cups are being shuffled! Watch carefully!"
            tourist_at_cup = False  # Tourist moves away during shuffling
            # Start shuffling
            generate_shuffle_sequence(15)
    
    elif game_state == "shuffling":
        shuffle_timer += 1
        if shuffle_timer >= shuffle_speed:
            shuffle_timer = 0
            perform_shuffle_move(current_shuffle_move)
            current_shuffle_move += 1
            if current_shuffle_move >= len(shuffle_moves):
                game_state = "betting"
                tourist_at_cup = True  # Tourist returns to their cup
                message = "A tourist has chosen a cup. You choose from the remaining cups."
    
    elif game_state == "reveal":
        # Ensure the ball is never under the selected cup (rigged game)
        if ball_position == selected_cup:
            # Find a cup that's not selected by player or tourist
            available_cups = [i for i in range(3) if i != selected_cup and i != tourist_cup]
            if available_cups:
                ball_position = available_cups[0]
            else:
                # Fallback if somehow both player and tourist selected the same cup
                ball_position = (selected_cup + 1) % 3
                
        message = f"The ball was under cup {ball_position+1}. You lost 10€!"
        player_money -= 10
        game_state = "result"

def main():
    """Main game loop"""
    global current_scene
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle input based on current scene
            if current_scene == SCENE_SQUARE:
                handle_square_input(event)
            elif current_scene == SCENE_DEMO:
                handle_demo_input(event)
            elif current_scene == SCENE_GAME:
                handle_game_input(event)
            elif current_scene == GAME_OVER:
                handle_game_over_input(event)
        
        # Update based on current scene
        if current_scene == SCENE_SQUARE:
            update_square()
        elif current_scene == SCENE_GAME:
            update_game()
        
        # Draw based on current scene
        if current_scene == SCENE_SQUARE:
            draw_scene_square()
        elif current_scene == SCENE_DEMO:
            draw_scene_demo()
        elif current_scene == SCENE_GAME:
            draw_scene_game()
        elif current_scene == GAME_OVER:
            draw_game_over()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
