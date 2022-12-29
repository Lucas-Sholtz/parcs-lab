from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        steps = self.read_input()
        worker_steps = steps / len(self.workers)

        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(i * worker_steps + 1, (i + 1) * worker_steps))
        reduced = self.myreduce(mapped)
        self.write_output(reduced)

    @staticmethod
    @expose
    def next_pi_multiplier(n):
        return(float(2*n)**2/float((2*n+1)*(2*n-1)))

    @staticmethod
    @expose
    def mymap(a, b):
        result = 1
        for n in range(a, b):
            result *= Solver.next_pi_multiplier(n)

        return result

    @staticmethod
    @expose
    def myreduce(mapped):
        # 2 because we have half of PI
        output = float(2)
        for x in mapped:
            output *= float(x.value)

        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line=f.readline()
        f.close()

        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str('{:.35f}'.format(output)))
        f.close()