import subprocess
import os
def evaluate(fen, depth, variations):
    #this is built for windows; you would need to use a different version of stockfish for another OS
    stockfish_path = os.path.join(os.path.dirname(__file__), "sf.exe")
    stockfish_process = subprocess.Popen([stockfish_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    #use one thread to ensure outputs are in order
    stockfish_process.stdin.write("setoption name Threads value 1\n")
    stockfish_process.stdin.write("setoption name UCI_Elo value 3190\n")
    stockfish_process.stdin.write("position fen " + str(fen) + "\n")
    stockfish_process.stdin.write("eval\n")
    stockfish_process.stdin.flush()
    evaluation = ""
    while True:
        line = stockfish_process.stdout.readline().strip()
        termination_string = "Final evaluation       "
        if line.find(termination_string) == 0:
            evaluation = line[len(termination_string)-1:].split()[0]
            break
    stockfish_process.stdin.write("setoption name MultiPV value " + str(variations) + "\n")
    stockfish_process.stdin.write("go depth " + str(depth) + "\n")
    stockfish_process.stdin.flush()
    output_lines = []
    while True:
        line = stockfish_process.stdout.readline().strip()
        #ignore this line since the best move and ponder is already in the variations
        if line.find("bestmove") == 0:
            break
        output_lines.append(line)
    stockfish_process.terminate()
    result_list = []
    for i in range(len(output_lines) - variations, len(output_lines)):
        line = output_lines[i].split()
        if (int(line[line.index("depth") + 1]) != depth):
            continue
        continuation = line[line.index("pv") + 1:]
        result_list.append(continuation)
    return result_list
