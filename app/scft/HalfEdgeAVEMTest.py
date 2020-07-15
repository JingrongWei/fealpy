#!/usr/bin/env python3

import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from fealpy.mesh import HalfEdgeMesh2d
from fealpy.opt.saddleoptalg import SteepestDescentAlg

from SCFTVEMModel2d import scftmodel2d_options, SCFTVEMModel2d
from vem2d_problem import halfedgemesh, init_mesh


class HalfEdgeAVEMTest():
    def __init__(self, mesh, fieldstype, moptions, optoptions):
        self.optoptions = optoptions
        obj = SCFTVEMModel2d(mesh, options=moptions)
        mu = obj.init_value(fieldstype=fieldstype)
        self.problem = {'objective': obj, 'mesh': mesh, 'x0': mu}

    def uni_run(self):
        problem = self.problem
        options = self.optoptions
        model = problem['objective']
        mesh = problem['mesh']

        optalg = SteepestDescentAlg(problem, options)
        optalg.run()

    def run(self, estimator='mix'):
        problem = self.problem
        options = self.optoptions
        model = problem['objective']


        optalg = SteepestDescentAlg(problem, options)
        x, f, g, diff = optalg.run(maxit=500)
        while True:
            while True:
                mesh = problem['mesh']
                aopts = mesh.adaptive_options(method='mean', maxcoarsen=3, HB=True)
                print('NN', mesh.number_of_nodes())
                mu = problem['x0']
                if estimator == 'mix':
                    eta = model.mix_estimate(mu, w=1)
                if estimator == 'grad':
                    eta = model.estimate(q)

                aopts['data'] = {'mu':mu}
                S0 = model.vemspace.project_to_smspace(aopts['data']['mu'][:,0])
                S1 = model.vemspace.project_to_smspace(aopts['data']['mu'][:,1])


                mesh.adaptive(eta, aopts)

                model.reinit(mesh)
                aopts['data']['mu'] = np.zeros((model.gdof,2))
                aopts['data']['mu'][:,0] = model.vemspace.interpolation(S0, aopts['HB'])
                aopts['data']['mu'][:,1] = model.vemspace.interpolation(S1, aopts['HB'])
                problem['x0'] = aopts['data']['mu']

                optalg = SteepestDescentAlg(problem, options)
                x, f, g, diff = optalg.run(maxit=100)
                problem['mesh'] = mesh
                problem['x0'] = x
                problem['rho'] = model.rho
                self.problem = problem

                if diff < options['FunValDiff']:
                   if (np.max(problem['rho'][:,0]) < 1) and (np.min(problem['rho'][:,0]) >0):
                       break
                pass


options = {
        'MaxIters': 5000,
        'MaxFunEvals': 5000,
        'NormGradTol': 1e-6,
        'FunValDiff': 1e-6,
        'StepLength': 2,
        'StepTol': 1e-14,
        'Output': True
        }

moptions = scftmodel2d_options(
        nspecies= 2,
        nblend = 1,
        nblock = 2,
        ndeg = 100,
        fA = 0.2,
        chiAB = 0.25,
        dim = 2,
        T0 = 20,
        T1 = 80,
        nupdate = 1,
        order = 1,
        rdir = sys.argv[1])

mesh = halfedgemesh(n=5, h=12)

Halftest = HalfEdgeAVEMTest(mesh, fieldstype=3, moptions=moptions,
        optoptions=options)

#Halftest.uni_run()
Halftest.run()
