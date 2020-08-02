from cvxopt import matrix, solvers

"""
A = matrix([ [-1.0, -1.0, 0.0, 1.0], [1.0, -1.0, -1.0, -2.0] ])
b = matrix([ 1.0, -2.0, 0.0, 4.0 ])
c = matrix([ 2.0, 1.0 ])
sol=solvers.lp(c,A,b)
print(sol)
"""

"""
c = matrix([-4., -5.])
G = matrix([[2., 1., -1., 0.], [1., 2., 0., -1.]])
h = matrix([3., 3., 0., 0.])
print(c)
print(G)
print(h)
sol = solvers.lp(c, G, h)
print(sol['x'])
"""
import test_data

constraints = [
			# Nutrients
			# f1  ,    f2,   f3, f1a, f1b, f2a, f2b, f3a, f3b, f1m, f2m, f3m
			[-614.0, -598.0, -52.0],
			[614.0, 598.0, 52.0],
			[-20.96, -20.96, -0.26],
			[20.96, 20.96, 0.26],
			[-55.5 , -52.54, -0.17],
			[55.5 , 52.54, 0.17],
		 	# Food items
		 	[1.0, 0.0, 0.0],
		 	[0.0, 1.0, 0.0],
		 	[0.0, 0.0, 1.0]
		  ]
almond_butter_constraints = [-614.0, 614.0, -60.96, 60.96, -1.0, 0.0, 0.0]
almonds_constraints =       [-598.0, 598.0, -20.96, 20.96, 0.0, -1.0, 0.0]
apple_constraints =         [-52.0, 52.0, -0.26, 0.26, 0.0, 0.0, -1.0]

constraints = [ almond_butter_constraints, almonds_constraints, apple_constraints ] #, apple_constraints ]

G = matrix(constraints)
h = matrix([-2900., 3520., -256., 300., 0.0, 0.0, 0.0]) #, -150.0, 16.0]), # 50, 250, 250])
c = matrix([614 + 60.96, 598 * 20.96, 52 * 0.26]) #,1.0])

print('c')
print(c)
print('G')
print(G)
print('h')
print(h)
sol = solvers.lp(c, G, h)
print(sol)
print(sol['x'])