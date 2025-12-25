import pygame
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.round_number = 1

        self.font = pygame.font.SysFont('Arial', 30)
        self.truths = [
            "Eevee belted 'Rattlin' Bog' while singing karaoke together.",
            "We rode a giant duck.",
            "We attended a beautiful wedding ceremony where 95% of the guests were sheep.",
            "We roasted marshmallows over an open fire.",
            "We bought live chickens for someone we don't know.",
            "We chased an oversized ball and always lost to a dog.",
            "We went gopher hunting at your local park, but went home empty handed.",
            "We stayed up late watching movies and eating snacks.",
            "We played pickle candy roulette and Malia tried to lose.",
            "We watched a child throw a rock at a giant's head.",
            "We witnessed a man tease a hawk swinging a treat attached to a string.",
            "We battled with squishmallows as our weapons.",
            "Baby Isaac frantically evaded a hidden beast at Robert and Malia's wedding.",
            "We went to a gator zoo and fed the gators hotdogs.",
            ]
        self.lies = [
            "Robert and Big Isaac retrieved a ball that Thor kicked onto the roof.",
            "We went skydiving together.",
            "We had a water drinking contest and Isaac and Robert tied.",
            "Robert stuck 4 full cupcakes in his mouth to demonstrate a political view to us.",
            "We had a book reading marathon that only lasted 10 minutes.",
            "Big Isaac lost Robert's car keys for three days.",
            "We built a fort out of sticks in Malia and Robert's backyard and the HOA fined us.",
            "We entered a dance competition and won first place.",
            "We went scuba diving in a bathtub.",
            "Tara and Malia taught us how to juggle flaming torches.",
            "Robert, Isaac, Malia, and Tara went trapeze jumping.",
            "We participated in a hot dog eating contest and Robert came in second place.",
            "We wore sheets and pretended to be ghosts at a fancy restaurant.",
            "We played water polo and Malia was the star player.",
            "We went on a road trip to find the world's largest rubber band ball.",
            "We attended a silent disco and danced the night away.",
            "We built a treehouse and filled it with books.",
            "We went on a treasure hunt and found a chest full of chocolate coins.",
            "We created math.",
            "We taught a parrot to recite Shakespearean sonnets.",
            "We invented a new color."
            "Isaac and Robert fought a homeless man for a sandwich.",
            "We entered a chili cook-off and won first place.",
            "We got lost in the desert and survived on cactus water.",
            "We built a raft and sailed down the Mississippi River.",
            "Baby Isaac rode a bull and Eevee and Thor flew an airplane.",
            "We attended a masquerade ball and danced with strangers.",
            "We went on a hot air balloon ride."
        ]
        
        self.statements, self.correct_truth = self.generate_round(self.truths, self.lies)

        self.selected_index = None

        self.submit_rect = pygame.Rect(300, 500, 200, 60)
        self.show_result = False
        self.was_correct = False

        self.next_rect = pygame.Rect(300, 500, 200, 60)
        
    def generate_round(self, truths, lies):
        truth = random.choice(truths)
        lie1, lie2 = random.sample(lies, 2)
        statements = [truth, lie1, lie2]
        random.shuffle(statements)
        return statements, truth
    
    def start_new_round(self):
        self.statements, self.correct_truth = self.generate_round(self.truths, self.lies)
        self.selected_index = None
        self.show_result = False
        self.was_correct = False
        self.round_number += 1
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.show_result:
                    # Only clickable on results screen
                    if self.next_rect.collidepoint(pos):
                        self.start_new_round()
                    return
                
                # Check if an answer was clicked
                for i, rect in enumerate(self.answer_rects):
                    if rect.collidepoint(pos):
                        self.selected_index = i

                # Check if submit button was clicked
                if self.submit_rect.collidepoint(pos) and self.selected_index is not None:
                    selected_statement = self.statements[self.selected_index]
                    self.was_correct = (selected_statement == self.correct_truth)
                    self.show_result = True
                    self.score += 1 if self.was_correct else 0

    def update(self):
        pass

    def render_wrapped_text(self, text, x, y, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for line in lines:
            surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(surface, (x, y))
            y += self.font.get_height()

    def draw(self):
        self.screen.fill((20, 20, 20))
        labels = ["a.", "b.", "c."]

        y = 100
        self.answer_rects = []

        #Draw score and round number
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        round_text = self.font.render(f"Round: {self.round_number}", True, (255, 255, 255))
        self.screen.blit(score_text, (50, 20)) 
        self.screen.blit(round_text, (650, 20))

        # Draw result if submitted
        if self.show_result:
            self.screen.fill((20, 20, 20))

            result = "Correct!" if self.was_correct else "Wrong!"
            self.render_wrapped_text(result, 50, 100, 700)

            truth_text = f"The truth was: {self.correct_truth}"
            self.render_wrapped_text(truth_text, 50, 180, 700)

            # Draw Next Round button
            pygame.draw.rect(self.screen, (100, 200, 100), self.next_rect)
            next_text = self.font.render("Next Round", True, (255, 255, 255))
            self.screen.blit(next_text, (self.next_rect.x + 20, self.next_rect.y + 10))

            pygame.display.flip()
            return


        for i, statement in enumerate(self.statements):
            label = labels[i]
            full_text = f"{label} {statement}"

            # --- WRAP THE TEXT ---
            words = full_text.split(" ")
            lines = []
            current = ""

            for word in words:
                test = current + word + " "
                if self.font.size(test)[0] <= 700:  # max width
                    current = test
                else:
                    lines.append(current)
                    current = word + " "
            lines.append(current)

            # Compute height of wrapped block
            block_height = len(lines) * self.font.get_height()

            # Create a clickable rect covering the whole block
            rect = pygame.Rect(50, y, 700, block_height)

            # Highlight if selected
            if self.selected_index == i:
                pygame.draw.rect(self.screen, (70, 70, 150), rect.inflate(10, 10))

            # Draw each wrapped line
            line_y = y
            for line in lines:
                surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(surface, (50, line_y))
                line_y += self.font.get_height()

            # Store rect for click detection
            self.answer_rects.append(rect)

            # Move down for next answer
            y += block_height + 40  # spacing

        # Draw submit button
        if not self.show_result:
            pygame.draw.rect(self.screen, (100, 200, 100), self.submit_rect)
            submit_text = self.font.render("Submit", True, (0, 0, 0))
            self.screen.blit(submit_text, (self.submit_rect.x + 50, self.submit_rect.y + 15))
        
        pygame.display.flip()


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()