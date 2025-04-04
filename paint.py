import pygame
import math

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Drawing App")
clock = pygame.time.Clock()

radius = 15
mode = 'blue'
tool = 'brush'
points = []
drawing = False
start_pos = None

while True:
    pressed = pygame.key.get_pressed()
    alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and (
                (event.key == pygame.K_w and ctrl_held) or 
                (event.key == pygame.K_F4 and alt_held) or 
                (event.key == pygame.K_ESCAPE))):
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = 'red'
            elif event.key == pygame.K_g:
                mode = 'green'
            elif event.key == pygame.K_b:
                mode = 'blue'
            elif event.key == pygame.K_e:
                tool = 'eraser'
            elif event.key == pygame.K_t:
                tool = 'rectangle'
            elif event.key == pygame.K_o:
                tool = 'circle'
            elif event.key == pygame.K_p:
                tool = 'brush'
            elif event.key == pygame.K_q:
                tool = 'square'
            elif event.key == pygame.K_y:
                tool = 'right_triangle'
            elif event.key == pygame.K_u:
                tool = 'equilateral_triangle'
            elif event.key == pygame.K_i:
                tool = 'rhombus'
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if tool in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                    start_pos = event.pos
                    drawing = True
                else:
                    radius = min(50, radius + 5)
            elif event.button == 3:
                radius = max(5, radius - 5)
        
        if event.type == pygame.MOUSEBUTTONUP:
            if tool in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                drawing = False
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos

                if tool == 'rectangle':
                    pygame.draw.rect(screen, pygame.Color(mode), pygame.Rect(start_pos, (x2 - x1, y2 - y1)))
                
                elif tool == 'circle':
                    center = ((x1 + x2) // 2, (y1 + y2) // 2)
                    radius_circle = max(abs(x2 - x1) // 2, abs(y2 - y1) // 2)
                    pygame.draw.circle(screen, pygame.Color(mode), center, radius_circle)
                
                elif tool == 'square':
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(screen, pygame.Color(mode), pygame.Rect(x1, y1, side, side))
                
                elif tool == 'right_triangle':
                    points_rt = [(x1, y1), (x2, y2), (x1, y2)]
                    pygame.draw.polygon(screen, pygame.Color(mode), points_rt)
                
                elif tool == 'equilateral_triangle':
                    side = abs(x2 - x1)
                    height = int(math.sqrt(3) / 2 * side)
                    top_vertex = (x1 + side // 2, y1)
                    left_vertex = (x1, y1 + height)
                    right_vertex = (x1 + side, y1 + height)
                    pygame.draw.polygon(screen, pygame.Color(mode), [top_vertex, left_vertex, right_vertex])
                
                elif tool == 'rhombus':
                    dx = (x2 - x1) // 2
                    dy = (y2 - y1) // 2
                    center = ((x1 + x2) // 2, (y1 + y2) // 2)
                    rhombus_points = [
                        (center[0], y1),
                        (x2, center[1]),
                        (center[0], y2),
                        (x1, center[1])
                    ]
                    pygame.draw.polygon(screen, pygame.Color(mode), rhombus_points)

        if event.type == pygame.MOUSEMOTION and tool == 'brush':
            position = event.pos
            points.append((position, mode, radius, tool))
            points = points[-256:]

    screen.fill((0, 0, 0))
    
    for point in points:
        pos, color, size, t = point
        if t == 'eraser':
            pygame.draw.circle(screen, (0, 0, 0), pos, size)
        else:
            pygame.draw.circle(screen, pygame.Color(color), pos, size)
    
    pygame.display.flip()
    clock.tick(60)
