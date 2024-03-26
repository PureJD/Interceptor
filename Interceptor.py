import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1500, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interceptor")

# Set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)  # For the countdown text and interceptors
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Center of the window
center_x, center_y = WIDTH // 2, HEIGHT // 2

interceptor_count = 50  # Initial count of interceptors

score = 0
max_interceptor_distance = 700 # Max distance an interceptor can travel
interceptors = []

# Square properties
square_size = 7
square_speed = 0.01  # Pixels per frame

# Font for displaying the countdown and accuracy
font = pygame.font.SysFont('Comic Sans', 21)


regeneration_interval = 5000  # 5000 milliseconds (5 seconds)
last_regeneration_time = pygame.time.get_ticks()  # Initial time

# Define the Square class
class Square:
    def __init__(self, x, y, speed, size, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.color = color

    def move_towards_center(self, center_x, center_y):
        dx = center_x - self.x
        dy = center_y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:  # Prevent division by zero
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist
        return dist

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

# Define the Interceptor class, inheriting from Square
class Interceptor(Square):
    def __init__(self, x, y, target_x, target_y, speed, size, color, accuracy):
        super().__init__(x, y, speed, size, color)
        self.original_x = x
        self.original_y = y
        self.distance_traveled = 0
        self.has_reached_target = False

        # Adjust target coordinates once based on accuracy modifier when the interceptor is created
        accuracy_modifier = WIDTH / 2 * (1 - accuracy / 100)
        self.adjusted_target_x = target_x + random.uniform(-accuracy_modifier, accuracy_modifier)
        self.adjusted_target_y = target_y + random.uniform(-accuracy_modifier, accuracy_modifier)

    def move_towards_target(self):
        dx = self.adjusted_target_x - self.x
        dy = self.adjusted_target_y - self.y
        dist = math.hypot(dx, dy)

        if dist < self.size or self.distance_traveled > max_interceptor_distance:
            self.has_reached_target = True
        else:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

        self.distance_traveled = math.hypot(self.x - self.original_x, self.y - self.original_y)



    


proximity_threshold = 0  # Distance within which an interceptor must be to a square to be considered near

# In the game loop, when checking if an interceptor has reached its target:
    




def calculate_accuracy(closest_distance):
    return max(0, min(100, 100 - (closest_distance / WIDTH * 100)))

def get_random_start_position():
    side = random.randint(0, 3)
    if side == 0:  # Left
        x = -square_size
        y = random.randint(0, HEIGHT)
    elif side == 1:  # Top
        x = random.randint(0, WIDTH)
        y = -square_size
    elif side == 2:  # Right
        x = WIDTH
        y = random.randint(0, HEIGHT)
    else:  # Bottom
        x = random.randint(0, WIDTH)
        y = HEIGHT
    return x, y

def generate_country():
    points = []
    num_points = 50
    base_radius = 200
    for i in range(num_points):
        angle = (2 * math.pi / num_points) * i
        radius_variation = random.randint(-20, 20)
        radius = base_radius + radius_variation
        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))
        points.append((x, y))
    return points

# Generate the terrain and squares
terrain = generate_country()
amount_of_squares = 20  # Adjust as needed
squares = [Square(*get_random_start_position(), square_speed, square_size, RED) for _ in range(amount_of_squares)]






# Game loop
running = True
while running:
    screen.fill(BLACK)  # Fill the screen with black
    # Calculate the closest square distance for accuracy calculation
    current_time = pygame.time.get_ticks()
    if squares:
        closest_square_distance = min((math.hypot(sq.x - center_x, sq.y - center_y) for sq in squares), default=0)
        accuracy = calculate_accuracy(closest_square_distance)
    else:
        closest_square_distance = 0
        accuracy = 0  # You might want to handle this case (no squares) differently

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Using spacebar to fire
                if squares and interceptor_count > 0:  # Ensure there are squares to target and interceptors are available
                    closest_square = min(squares, key=lambda sq: (sq.x - center_x)**2 + (sq.y - center_y)**2)
                    # Use the current game accuracy for the newly created interceptor
                    interceptors.append(Interceptor(center_x, center_y, closest_square.x, closest_square.y, square_speed, square_size, WHITE, accuracy))
                    interceptor_count -= 1


    
    
    # Interceptor regeneration mechanism
    if current_time - last_regeneration_time >= regeneration_interval:
        interceptor_count += 1  # Increment the count of interceptors
        last_regeneration_time = current_time  # Reset the last regeneration time
    




    for interceptor in interceptors:
        interceptor.move_towards_target()  # Use the modified move method for interceptors
        interceptor.draw(screen)
        if interceptor.distance_traveled > max_interceptor_distance:
            interceptors.remove(interceptor)
        interceptor.draw(screen)
    
    for interceptor in interceptors[:]:  # Use a copy for safe removal
    # Move towards the adjusted target coordinates
        dx = interceptor.adjusted_target_x - interceptor.x
        dy = interceptor.adjusted_target_y - interceptor.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            interceptor.x += interceptor.speed * dx / dist
            interceptor.y += interceptor.speed * dy / dist
            interceptor.distance_traveled = math.hypot(interceptor.x - interceptor.original_x, interceptor.y - interceptor.original_y)

        # Check if the interceptor has reached its target or exceeded the maximum allowed distance
        if interceptor.has_reached_target or interceptor.distance_traveled > max_interceptor_distance:
            interceptors.remove(interceptor)
        else:
            interceptor.draw(screen)



    # Update squares and calculate the maximum distance from the center
    if squares:  # Check if there are squares to update
        max_distance = max(square.move_towards_center(center_x, center_y) for square in squares)
        # Estimate the countdown time (distance / speed)
        countdown_time = max_distance / (square_speed * 60)  # Convert to seconds
    else:
        countdown_time = 0  # Set to 0 if there are no squares


    for square in squares:  # Draw each square
        square.draw(screen)

    pygame.draw.lines(screen, WHITE, True, terrain, 4)  # Draw the terrain

    
    # Render the countdown time
    if countdown_time > 700:
        countdown_text = font.render(f'Proximity till impact: {countdown_time:.2f}', True, WHITE)
    else:
        countdown_text = font.render(f'Proximity till impact: {countdown_time:.2f}', True, RED)
    screen.blit(countdown_text, (50, 50))

    # Render the accuracy percentage
    if accuracy > 90:
        accuracy_text = font.render(f'Accuracy: {accuracy:.0f}%', True, BLUE)
    elif accuracy >= 80 and accuracy <= 90:
        accuracy_text = font.render(f'Accuracy: {accuracy:.0f}%', True, GREEN)
    elif accuracy < 80:
        accuracy_text = font.render(f'Accuracy: {accuracy:.0f}%', True, RED)
    screen.blit(accuracy_text, (WIDTH - 200, 50))

    show_sccore = font.render(f'Score: {score}', True, WHITE)
    screen.blit(show_sccore, (WIDTH - 200, 20))

    if interceptor_count > 40:
        interceptor_text = font.render(f'Interceptors: {interceptor_count}', True, BLUE)
    elif interceptor_count >= 10 and interceptor_count < 21:
        interceptor_text = font.render(f'Interceptors: {interceptor_count}', True, GREEN)
    elif interceptor_count < 10:
        interceptor_text = font.render(f'Interceptors: {interceptor_count}', True, RED)
    screen.blit(interceptor_text, (WIDTH - 200, 80))  # Adjust position as needed

    for interceptor in interceptors[:]:  # Use a copy for safe removal
        interceptor.move_towards_target()
        interceptor_rect = pygame.Rect(interceptor.x, interceptor.y, interceptor.size, interceptor.size)
        for square in squares[:]:
            square_rect = pygame.Rect(square.x, square.y, square.size, square.size)
            if interceptor_rect.colliderect(square_rect):
                score += 100  # Update the score
                squares.remove(square)  # Remove the square on collision

            # Draw the interceptor if it's still active
            interceptor.draw(screen)

   


    if countdown_time <= 0:
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (center_x - 50, center_y - 10))
    pygame.display.flip()  # Update the display 
    

pygame.quit()
sys.exit()

