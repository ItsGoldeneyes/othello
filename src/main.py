from othello import OthelloGame
import pickle
import time
import neat
import os


class Othello:
    
    def bucket_output(self, output):
        return (int((output[0]*10)/1.25), int((output[1]*10)/1.25))
        
    def test_ai(self, net):
        game = OthelloGame()
        game.show()
        player = 1
        
        while not game.winner:
            if player == 1:
                game.turn(player)
            else:
                output = net.activate(tuple([player]+game.get_info()))
                decision = self.bucket_output(output)
                
                game.turn(player, decision)
                
            game.show()
            player = (player%2)+1

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2
        
        game = OthelloGame(debug=False)
        # game.show()
        player = 1
        fail_timer = 0
        while not game.winner:
            # time.sleep(0.1)
            if player == 1:
                output = net1.activate(tuple([(player)]+game.get_info()))
                decision = self.bucket_output(output)
                # print(decision)
                turn_result = game.turn(player, decision)
            else:
                output = net2.activate(tuple([player]+game.get_info()))
                decision = self.bucket_output(output)
                # print(decision)
                
                turn_result = game.turn(player, decision)
                
            if turn_result == False:
                fail_timer += 1
            else:
                fail_timer = 0
                
            if fail_timer >= 2:
                break
        
            player = (player%2)+1
            # game.show()
        
        self.calculate_fitness(genome1, genome2, game.get_fitness())
         
    def calculate_fitness(self, genome1, genome2, fitness):
        if fitness[0] < 3:
            genome1.fitness -= 1
            
        if fitness[1] < 3:
            genome1.fitness -= 1
        
        genome1.fitness += fitness[0]/10
        genome1.fitness += fitness[2]/10
        genome2.fitness += fitness[1]/5
        genome2.fitness += fitness[3]/5
        

def eval_genomes(genomes, config):
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            
            game = Othello()
            game.train_ai(genome1, genome2, config)
            
def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50) #50
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    run_neat(config)