#!/usr/bin/env python3

# ========================================================================
#
# Imports
#
# ========================================================================
import argparse
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml

# ========================================================================
#
# Some defaults variables
#
# ========================================================================
plt.rc('text', usetex=True)
plt.rc('font', family='serif', serif='Times')
cmap_med = ['#F15A60', '#7AC36A', '#5A9BD4', '#FAA75B',
            '#9E67AB', '#CE7058', '#D77FB4', '#737373']
cmap = ['#EE2E2F', '#008C48', '#185AA9', '#F47D23',
        '#662C91', '#A21D21', '#B43894', '#010202']
dashseq = [(None, None), [10, 5], [10, 4, 3, 4], [
    3, 3], [10, 4, 3, 4, 3, 4], [3, 3], [3, 3]]
markertype = ['s', 'd', 'o', 'p', 'h']


# ========================================================================
#
# Function definitions
#
# ========================================================================
def parse_ic(fname):
    """Parse the Nalu yaml input file for the initial conditions"""
    with open(fname, 'r') as stream:
        try:
            dat = yaml.load(stream)
            u0 = float(dat['realms'][0]['initial_conditions']
                       [0]['value']['velocity'][0])
            rho0 = float(dat['realms'][0]['material_properties']
                         ['specifications'][0]['value'])
            mu = float(dat['realms'][0]['material_properties']
                       ['specifications'][1]['value'])

            return u0, rho0, mu

        except yaml.YAMLError as exc:
            print(exc)


# ========================================================================
def get_uref(fname):
    """Read a Nalu velocity probe file and get the reference velocity.

    This is done at the center of the channel (z=5).
    """
    ulst = []
    with open(fname) as f:
        for line in f:
            line = line.split()

            # Get the time step and time
            if len(line) == 2:
                step = int(line[0])
                time = float(line[1])

            if len(line) == 6 and 'Coordinates' not in line[0]:
                ulst.append([step,
                             time,
                             float(line[0]),
                             float(line[1]),
                             float(line[2]),
                             float(line[3]),
                             float(line[4]),
                             float(line[5])])

    # Create dataframe
    df = pd.DataFrame(ulst,
                      columns=['step', 'time', 'x', 'y', 'z', 'u', 'v', 'w'])
    df = df.drop_duplicates()
    df = df.sort_values(by=['step', 'z'])

    subdf = df[np.fabs(df['step'] - np.max(df['step'])) < 1e-14]
    idx = np.argmin(np.fabs(subdf['z'] - 5.0))
    return subdf.loc[idx]['u']


# ========================================================================
def parse_velocity_probe(fname, uref):
    """Read a Nalu velocity probe file."""

    ulst = []
    relst = []
    with open(fname) as f:
        for line in f:
            line = line.split()

            # Get the time step and time
            if len(line) == 2:
                step = int(line[0])
                time = float(line[1])

            if len(line) == 6 and 'Coordinates' not in line[0]:
                ulst.append([step,
                             time,
                             float(line[0]),
                             float(line[1]),
                             float(line[2]),
                             float(line[3]),
                             float(line[4]),
                             float(line[5])])

            if len(line) == 9 and 'Coordinates' not in line[0]:
                relst.append([step,
                              time,
                              float(line[0]),
                              float(line[1]),
                              float(line[2]),
                              float(line[3]),
                              float(line[4]),
                              float(line[5]),
                              float(line[6]),
                              float(line[7]),
                              float(line[8])])

    # Create dataframes
    df = pd.DataFrame(ulst,
                      columns=['step', 'time', 'x', 'y', 'z', 'u', 'v', 'w'])
    df = df.drop_duplicates()
    df = df.sort_values(by=['step', 'z'])

    redf = pd.DataFrame(relst,
                        columns=['step', 'time', 'x', 'y', 'z', 'uu', 'uv', 'uw', 'vv', 'vw', 'ww'])
    redf = redf.drop_duplicates()
    redf = redf.sort_values(by=['step', 'z'])

    # Merge all together
    df = pd.merge(df, redf, on=['step', 'time', 'x', 'y', 'z'])

    # Non-dimensionalize some quantities
    df['u'] = df['u'] / uref
    df['v'] = df['v'] / uref
    df['w'] = df['w'] / uref
    df['uu'] = df['uu'] / uref**2
    df['uv'] = df['uv'] / uref**2
    df['uw'] = df['uw'] / uref**2
    df['vv'] = df['vv'] / uref**2
    df['vw'] = df['vw'] / uref**2
    df['ww'] = df['ww'] / uref**2
    return df.reset_index(drop=True)


# ========================================================================
def parse_wall_probe(fname, yname):
    """Read a Nalu wall probe file."""

    tlst = []
    plst = []
    with open(fname) as f:
        for line in f:
            line = line.split()

            # Get the time step and time
            if len(line) == 2:
                step = int(line[0])
                time = float(line[1])

            if len(line) == 4:

                if 'tau_wall' in line[3]:
                    tau_wall = True
                    pressure = False

                elif 'pressure' in line[3]:
                    pressure = True
                    tau_wall = False

                else:
                    if tau_wall:
                        tlst.append([step,
                                     time,
                                     float(line[0]),
                                     float(line[1]),
                                     float(line[2]),
                                     float(line[3])])

                    elif pressure:
                        plst.append([step,
                                     time,
                                     float(line[0]),
                                     float(line[1]),
                                     float(line[2]),
                                     float(line[3])])

        # Create dataframes
        df = pd.DataFrame(tlst,
                          columns=['step', 'time', 'x', 'y', 'z', 'tau_wall'])
        pdf = pd.DataFrame(plst,
                           columns=['step', 'time', 'x', 'y', 'z', 'pressure'])
        df['pressure'] = pdf['pressure']
        df = df.drop_duplicates()
        df = df.sort_values(by=['step', 'x']).reset_index(drop=True)

        # Calculate coefficients
        u0, rho0, mu = parse_ic(yname)
        dynPres = rho0 * 0.5 * u0 * u0
        df['cf'] = df['tau_wall'] / dynPres
        df['cp'] = df['pressure'] / dynPres
        df['cp_orig'] = df['pressure'] / dynPres

    return df


# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == '__main__':

    # ========================================================================
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='A simple plot tool')
    parser.add_argument(
        '-s', '--show', help='Show the plots', action='store_true')
    args = parser.parse_args()

    # ======================================================================
    # NASA experiment
    fname = os.path.join(os.path.abspath('nasa_data'), 'profiles_exp.dat')
    df = pd.read_csv(fname, comment='#')

    # x = -4
    subdf = df[np.fabs(df['x'] - (-4.0)) < 1e-14]
    plt.figure(0)
    p = plt.plot(subdf['u'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=-4')

    plt.figure(1)
    p = plt.plot(subdf['uv'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=-4')

    # x = 1
    subdf = df[np.fabs(df['x'] - (1.0)) < 1e-14]
    plt.figure(2)
    p = plt.plot(subdf['u'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=1')

    plt.figure(3)
    p = plt.plot(subdf['uv'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=1')

    # x = 4
    subdf = df[np.fabs(df['x'] - (4.0)) < 1e-14]
    plt.figure(4)
    p = plt.plot(subdf['u'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=4')

    plt.figure(5)
    p = plt.plot(subdf['uv'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=4')

    # x = 6
    subdf = df[np.fabs(df['x'] - (6.0)) < 1e-14]
    plt.figure(6)
    p = plt.plot(subdf['u'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=6')

    plt.figure(7)
    p = plt.plot(subdf['uv'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=6')

    # x = 10
    subdf = df[np.fabs(df['x'] - (10.0)) < 1e-14]
    plt.figure(8)
    p = plt.plot(subdf['u'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=10')

    plt.figure(9)
    p = plt.plot(subdf['uv'], subdf['y'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp. x=10')

    # Cp
    fname = os.path.join(os.path.abspath('nasa_data'), 'cp_lower_exp.dat')
    df = pd.read_csv(fname, comment='#')

    plt.figure(10)
    p = plt.plot(df['x'], df['cp'], ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp.')

    # Cf
    fname = os.path.join(os.path.abspath('nasa_data'), 'cf_lower_exp.dat')
    df = pd.read_csv(fname, comment='#')

    plt.figure(11)
    p = plt.plot(df['x'], np.fabs(df['cf']), ls='-', lw=1, color=cmap[-1],
                 marker=markertype[0], mec=cmap[-1], mfc=cmap[-1], ms=6,
                 label='Exp.')

    # ======================================================================
    # NASA CFL3D
    fname = os.path.join(os.path.abspath('nasa_data'), 'u_profiles_cfl3d.dat')
    udf = pd.read_csv(fname, comment='#')
    fname = os.path.join(os.path.abspath('nasa_data'), 'uv_profiles_cfl3d.dat')
    uvdf = pd.read_csv(fname, comment='#')

    # x = -4
    subdf = udf[np.fabs(udf['x'] - (-4.0)) < 1e-14]
    plt.figure(0)
    p = plt.plot(subdf['u'], subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D x=-4')
    p[0].set_dashes(dashseq[0])

    subdf = uvdf[np.fabs(uvdf['x'] - (-3.953960419)) < 1e-14]
    plt.figure(1)
    p = plt.plot(subdf['uv'] * 1000, subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D. x=-4')
    p[0].set_dashes(dashseq[0])

    # x = 1
    subdf = udf[np.fabs(udf['x'] - 1.0) < 1e-14]
    plt.figure(2)
    p = plt.plot(subdf['u'], subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D x=1')
    p[0].set_dashes(dashseq[0])

    subdf = uvdf[np.fabs(uvdf['x'] - 1.0) < 1e-14]
    plt.figure(3)
    p = plt.plot(subdf['uv'] * 1000, subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D. x=1')
    p[0].set_dashes(dashseq[0])

    # x = 4
    subdf = udf[np.fabs(udf['x'] - 4.0) < 1e-14]
    plt.figure(4)
    p = plt.plot(subdf['u'], subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D x=4')
    p[0].set_dashes(dashseq[0])

    subdf = uvdf[np.fabs(uvdf['x'] - 4.0) < 1e-14]
    plt.figure(5)
    p = plt.plot(subdf['uv'] * 1000, subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D. x=4')
    p[0].set_dashes(dashseq[0])

    # x = 6
    subdf = udf[np.fabs(udf['x'] - 6.0) < 1e-14]
    plt.figure(6)
    p = plt.plot(subdf['u'], subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D x=6')
    p[0].set_dashes(dashseq[0])

    subdf = uvdf[np.fabs(uvdf['x'] - 6.0) < 1e-14]
    plt.figure(7)
    p = plt.plot(subdf['uv'] * 1000, subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D. x=6')
    p[0].set_dashes(dashseq[0])

    # x = 10
    subdf = udf[np.fabs(udf['x'] - 10.0) < 1e-14]
    plt.figure(8)
    p = plt.plot(subdf['u'], subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D x=10')
    p[0].set_dashes(dashseq[0])

    subdf = uvdf[np.fabs(uvdf['x'] - 10.0) < 1e-14]
    plt.figure(9)
    p = plt.plot(subdf['uv'] * 1000, subdf['y'], lw=2,
                 color=cmap[0], label='CFL3D. x=10')
    p[0].set_dashes(dashseq[0])

    # Cp
    fname = os.path.join(os.path.abspath('nasa_data'), 'cp_lower_cfl3d.dat')
    df = pd.read_csv(fname, comment='#')

    plt.figure(10)
    p = plt.plot(df['x'], df['cp'], lw=2, color=cmap[0], label='CFL3D')
    p[0].set_dashes(dashseq[0])

    # Cf
    fname = os.path.join(os.path.abspath('nasa_data'), 'cf_lower_cfl3d.dat')
    df = pd.read_csv(fname, comment='#')

    plt.figure(11)
    p = plt.plot(df['x'], np.fabs(df['cf']), lw=2,
                 color=cmap[0], label='CFL3D')
    p[0].set_dashes(dashseq[0])

    # ======================================================================
    # Nalu output
    fdir = os.path.abspath('513')
    rdir = os.path.abspath(os.path.join(fdir, 'results'))
    yname = os.path.join(fdir, 'backStep.i')

    # x = -4
    fname = os.path.join(rdir, 'probe_profile0_0.dat')
    uref = get_uref(fname)
    df = parse_velocity_probe(fname, uref)
    print(np.unique(df['step']), np.unique(df['time']))
    subdf = df[np.fabs(df['step'] - np.max(df['step'])) < 1e-14]

    plt.figure(0)
    p = plt.plot(subdf['u'], subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=-4')
    p[0].set_dashes(dashseq[1])

    plt.figure(1)
    p = plt.plot(subdf['uw'] * 1000, subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=-4')
    p[0].set_dashes(dashseq[1])

    # x = 1
    fname = os.path.join(rdir, 'probe_profile1_0.dat')
    df = parse_velocity_probe(fname, uref)
    subdf = df[np.fabs(df['step'] - np.max(df['step'])) < 1e-14]

    plt.figure(2)
    p = plt.plot(subdf['u'], subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=1')
    p[0].set_dashes(dashseq[1])

    plt.figure(3)
    p = plt.plot(subdf['uw'] * 1000, subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=1')
    p[0].set_dashes(dashseq[1])

    # x = 4
    fname = os.path.join(rdir, 'probe_profile2_0.dat')
    df = parse_velocity_probe(fname, uref)
    subdf = df[np.fabs(df['step'] - np.max(df['step'])) < 1e-14]

    plt.figure(4)
    p = plt.plot(subdf['u'], subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=4')
    p[0].set_dashes(dashseq[1])

    plt.figure(5)
    p = plt.plot(subdf['uw'] * 1000, subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=4')
    p[0].set_dashes(dashseq[1])

    # x = 6
    fname = os.path.join(rdir, 'probe_profile3_0.dat')
    df = parse_velocity_probe(fname, uref)
    subdf = df[np.fabs(df['step'] - np.max(df['step'])) < 1e-14]

    plt.figure(6)
    p = plt.plot(subdf['u'], subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=6')
    p[0].set_dashes(dashseq[1])

    plt.figure(7)
    p = plt.plot(subdf['uw'] * 1000, subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=6')
    p[0].set_dashes(dashseq[1])

    # x = 10
    fname = os.path.join(rdir, 'probe_profile4_0.dat')
    df = parse_velocity_probe(fname, uref)
    subdf = df[np.fabs(df['step'] - np.max(df['step'])) < 1e-14]

    plt.figure(8)
    p = plt.plot(subdf['u'], subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=10')
    p[0].set_dashes(dashseq[1])

    plt.figure(9)
    p = plt.plot(subdf['uw'] * 1000, subdf['z'], ls='-', lw=2, color=cmap[1],
                 label='Nalu x=10')
    p[0].set_dashes(dashseq[1])

    # Cp and Cf (before and after the step)
    fname = os.path.join(rdir, 'probe_backbottomwall_0.dat')
    bdf = parse_wall_probe(fname, yname)
    fname = os.path.join(rdir, 'probe_frontbottomwall_1.dat')
    fdf = parse_wall_probe(fname, yname)
    df = pd.concat([bdf, fdf])
    df = df.drop_duplicates()
    df = df[df['x'] != 0]
    df = df.sort_values(by=['step', 'x']).reset_index(drop=True)

    subdf = df[np.fabs(df['step'] - np.max(df['step'])) < 1e-14]

    plt.figure(10)
    p = plt.plot(subdf['x'], subdf['cp'], ls='-', lw=2, color=cmap[1],
                 label='Nalu')
    p[0].set_dashes(dashseq[1])

    plt.figure(11)
    p = plt.plot(subdf['x'], subdf['cf'], ls='-', lw=2, color=cmap[1],
                 label='Nalu')
    p[0].set_dashes(dashseq[1])

    # ======================================================================
    # Format the plots
    plt.figure(0)
    ax = plt.gca()
    plt.xlabel(r"$u / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([0, 1.2])
    ax.set_ylim([1, 5])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('u_m4.pdf', format='pdf')
    plt.savefig('u_m4.png', format='png')

    plt.figure(1)
    ax = plt.gca()
    plt.xlabel(r"$1000 \times u'v' / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-1.5, 0.5])
    ax.set_ylim([1, 5])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('uv_m4.pdf', format='pdf')
    plt.savefig('uv_m4.png', format='png')

    plt.figure(2)
    ax = plt.gca()
    plt.xlabel(r"$u / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-0.4, 1.2])
    ax.set_ylim([0, 3])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('u_1.pdf', format='pdf')
    plt.savefig('u_1.png', format='png')

    plt.figure(3)
    ax = plt.gca()
    plt.xlabel(r"$1000 \times u'v' / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-15, 5])
    ax.set_ylim([0, 3])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('uv_1.pdf', format='pdf')
    plt.savefig('uv_1.png', format='png')

    plt.figure(4)
    ax = plt.gca()
    plt.xlabel(r"$u / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-0.4, 1.2])
    ax.set_ylim([0, 3])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('u_4.pdf', format='pdf')
    plt.savefig('u_4.png', format='png')

    plt.figure(5)
    ax = plt.gca()
    plt.xlabel(r"$1000 \times u'v' / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-15, 5])
    ax.set_ylim([0, 3])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('uv_4.pdf', format='pdf')
    plt.savefig('uv_4.png', format='png')

    plt.figure(6)
    ax = plt.gca()
    plt.xlabel(r"$u / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-0.4, 1.2])
    ax.set_ylim([0, 3])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('u_6.pdf', format='pdf')
    plt.savefig('u_6.png', format='png')

    plt.figure(7)
    ax = plt.gca()
    plt.xlabel(r"$1000 \times u'v' / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-15, 5])
    ax.set_ylim([0, 3])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('uv_6.pdf', format='pdf')
    plt.savefig('uv_6.png', format='png')

    plt.figure(8)
    ax = plt.gca()
    plt.xlabel(r"$u / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-0.4, 1.2])
    ax.set_ylim([0, 3])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('u_10.pdf', format='pdf')
    plt.savefig('u_10.png', format='png')

    plt.figure(9)
    ax = plt.gca()
    plt.xlabel(r"$1000 \times u'v' / u_r$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$y$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-15, 5])
    ax.set_ylim([0, 3])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('uv_10.pdf', format='pdf')
    plt.savefig('uv_10.png', format='png')

    plt.figure(10)
    ax = plt.gca()
    plt.xlabel(r"$x$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$C_p$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-5, 30])
    ax.set_ylim([-0.3, 0.1])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('cp.pdf', format='pdf')
    plt.savefig('cp.png', format='png')

    plt.figure(11)
    ax = plt.gca()
    plt.xlabel(r"$x$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$|C_f|$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    ax.set_xlim([-5, 30])
    ax.set_ylim([-0.002, 0.004])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('cf.pdf', format='pdf')
    plt.savefig('cf.png', format='png')

    if args.show:
        plt.show()
