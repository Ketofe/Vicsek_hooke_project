import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from find_group_index import * 


#Made using chat gpt, I have edited a little bit
def Animate_c(pos, theta, colors,proportions, number_of_frames,  interval=1,black_index=None , trace_index=None):
    fig, ax = plt.subplots(figsize=(6, 6))

    #The number of particles
    N=len(pos[0])

    
    
    Index_limit_of_each_group=[] 
    limit_index=0
    for p in proportions:
         limit_index=N*p+limit_index
         Index_limit_of_each_group.append(limit_index)
    Index_limit_of_each_group=np.array(Index_limit_of_each_group)

    # Set up the initial quiver plot
    qv = ax.quiver(pos[0][:, 0], pos[0][:, 1], np.cos(theta[0]), np.sin(theta[0]))
    
    # Optional: Line for tracing the path of the trace_index
    if trace_index is not None:
        trace_path_x, trace_path_y = [], []
        trace_line, = ax.plot([], [], color='red', lw=2, label=f'Trace of index {trace_index}')
    
    # Setting plot limits (you can adjust according to your needs)
    ax.set_xlim(np.min(pos) - 1, np.max(pos) + 1)
    ax.set_ylim(np.min(pos) - 1, np.max(pos) + 1)
    
    # Animation function
    def animate(i):
        # Update the position and direction of the quivers
        qv.set_offsets(pos[i])
        qv.set_UVC(np.cos(theta[i]), np.sin(theta[i]))

        # Update the colors based on the index
        c = np.array(['black' if idx == black_index else colors[find_group_index(Index_limit_of_each_group,idx)] for idx in range(N)])
        qv.set_color(c)

        # Update the trace path if trace_index is provided
        if trace_index is not None:
            trace_path_x.append(pos[i][trace_index, 0])
            trace_path_y.append(pos[i][trace_index, 1])
            trace_line.set_data(trace_path_x, trace_path_y)
        
        return (qv, trace_line) if trace_index is not None else (qv,)

    # Run the animation
    anim = FuncAnimation(fig, animate, np.arange(1, number_of_frames), interval=interval, blit=True)
    
    # Add a legend if trace path is shown
    if trace_index is not None:
        ax.legend()
    
    plt.show()
    return anim