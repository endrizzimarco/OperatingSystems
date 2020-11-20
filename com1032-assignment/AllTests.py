import unittest
import tests.PriorityTest as test1
import tests.RoundRobinTest as test2
import tests.AllocationTest as test3
import tests.PageSwappingTest as test4


loader = unittest.TestLoader()
suite  = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test1))
suite.addTests(loader.loadTestsFromModule(test2))
suite.addTests(loader.loadTestsFromModule(test3))
suite.addTests(loader.loadTestsFromModule(test4))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
