import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path
import numpy as np
import math

def draw_pct_hierarchy(levels=3, columns_per_level=None, unit_size=1.0, 
                      level_spacing=4.0, column_spacing=2.5, 
                      filename="pct_hierarchy.png", figsize=(12, 8), use_arrows=True, 
                      font_color='black', unit_line_width=0.8, inter_level_arrows=True,
                      show_title=False, show_legend=False, arrow_length_factor=0.1,
                      curve_control_factor=0.6, curve_line_width=1.0, curve_alpha=0.9, 
                      curve_resolution=100, arrowhead_size=1.0, arrowhead_style='-|>'):
    """
    Generate a configurable PCT hierarchy diagram.
    
    Parameters:
    -----------
    levels : int
        Number of hierarchy levels
    columns_per_level : list or None  
        Number of columns per level. If None, defaults to [4, 2, 1] pattern
    unit_size : float
        Size of the circles in each unit
    level_spacing : float
        Vertical spacing between levels
    column_spacing : float
        Horizontal spacing between columns
    filename : str
        Output filename for the image
    figsize : tuple
        Figure size (width, height)
    use_arrows : bool
        If True, use arrows between circles. If False, use simple lines between centers.
    font_color : str
        Color of the letters inside the circles (default: 'white')
    unit_line_width : float
        Line width for connections within each PCT unit (default: 1.5)
    inter_level_arrows : bool
        If True, add arrowheads to connections between levels (default: True)
    show_title : bool
        If True, display the title above the diagram (default: True)
    show_legend : bool
        If True, display the legend with circle color meanings (default: True)
    arrow_length_factor : float
        Multiplier for arrow length relative to unit_size (default: 0.5)
    curve_control_factor : float
        Controls S-curve shape - larger values create more pronounced curves (default: 0.3)
    curve_line_width : float
        Line width for S-curve connections between levels (default: 1.0)
    curve_alpha : float
        Transparency for S-curve connections (0.0=transparent, 1.0=opaque, default: 0.7)
    curve_resolution : int
        Number of points used to draw smooth S-curves (default: 100)
    arrowhead_size : float
        Size multiplier for inter-level arrowheads relative to unit_size (default: 0.3)
    arrowhead_style : str
        Style of the arrowheads - options: '-|>' (wedge), '->' (simple), '->|' (bar), 
        '<->', '<|-|>', 'fancy', 'simple', 'wedge' (default: '-|>')
    """
    
    if columns_per_level is None:
        # Default pattern: decrease by half each level
        columns_per_level = []
        cols = 4
        for i in range(levels):
            columns_per_level.append(max(1, cols))
            cols = max(1, cols // 2)
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')
    
    # Colors for different circle types
    colors = {
        'reference': 'red',
        'comparator': 'orange', 
        'output': 'green',
        'perception': 'aqua'
    }
    
    # Store positions for drawing connections
    unit_positions = {}
    
    def draw_unit(center_x, center_y, level, col):
        """Draw a single PCT unit with 4 circles and internal arrows"""
        
        # Calculate positions of the 4 circles
        # Comparator in center
        comp_x, comp_y = center_x, center_y
        
        # Other circles at specified angles around the comparator
        radius = unit_size * 0.8
        ref_x = comp_x + radius * math.cos(math.radians(90))     # Reference at top (90°)
        ref_y = comp_y + radius * math.sin(math.radians(90))
        
        out_x = comp_x + radius * math.cos(math.radians(330))    # Output at bottom right (330°)
        out_y = comp_y + radius * math.sin(math.radians(330))
        
        perc_x = comp_x + radius * math.cos(math.radians(210))   # Perception at bottom left (210°)
        perc_y = comp_y + radius * math.sin(math.radians(210))
        
        # Draw circles
        circles = {
            'reference': plt.Circle((ref_x, ref_y), unit_size*0.15, 
                                  color=colors['reference'], zorder=3),
            'comparator': plt.Circle((comp_x, comp_y), unit_size*0.15, 
                                   color=colors['comparator'], zorder=3),
            'output': plt.Circle((out_x, out_y), unit_size*0.15, 
                               color=colors['output'], zorder=3),
            'perception': plt.Circle((perc_x, perc_y), unit_size*0.15, 
                                   color=colors['perception'], zorder=3)
        }
        
        for circle in circles.values():
            ax.add_patch(circle)
        
        # Add first letter labels to circles
        text_props = dict(ha='center', va='center', fontsize=8, fontweight='bold', 
                         color=font_color, zorder=4)
        
        ax.text(ref_x, ref_y, 'r', **text_props)      # Reference
        ax.text(comp_x, comp_y, 'c', **text_props)    # Comparator
        ax.text(out_x, out_y, 'o', **text_props)      # Output
        ax.text(perc_x, perc_y, 'p', **text_props)    # Perception
        
        # Draw internal connections (arrows or simple lines)
        if use_arrows:
            # Draw arrows (avoiding circle overlap)
            arrow_props = dict(arrowstyle='->', lw=unit_line_width, color='black', zorder=2)
            circle_radius = unit_size * 0.15
            
            # Reference -> Comparator (from top to center)
            ref_to_comp_dx = comp_x - ref_x
            ref_to_comp_dy = comp_y - ref_y
            ref_to_comp_dist = math.sqrt(ref_to_comp_dx**2 + ref_to_comp_dy**2)
            ref_start_x = ref_x + (ref_to_comp_dx / ref_to_comp_dist) * circle_radius
            ref_start_y = ref_y + (ref_to_comp_dy / ref_to_comp_dist) * circle_radius
            comp_end_x = comp_x - (ref_to_comp_dx / ref_to_comp_dist) * circle_radius
            comp_end_y = comp_y - (ref_to_comp_dy / ref_to_comp_dist) * circle_radius
            
            ax.annotate('', xy=(comp_end_x, comp_end_y), 
                       xytext=(ref_start_x, ref_start_y),
                       arrowprops=arrow_props)
            
            # Perception -> Comparator (from bottom left to center)
            perc_to_comp_dx = comp_x - perc_x
            perc_to_comp_dy = comp_y - perc_y
            perc_to_comp_dist = math.sqrt(perc_to_comp_dx**2 + perc_to_comp_dy**2)
            perc_start_x = perc_x + (perc_to_comp_dx / perc_to_comp_dist) * circle_radius
            perc_start_y = perc_y + (perc_to_comp_dy / perc_to_comp_dist) * circle_radius
            comp_end2_x = comp_x - (perc_to_comp_dx / perc_to_comp_dist) * circle_radius
            comp_end2_y = comp_y - (perc_to_comp_dy / perc_to_comp_dist) * circle_radius
            
            ax.annotate('', xy=(comp_end2_x, comp_end2_y), 
                       xytext=(perc_start_x, perc_start_y),
                       arrowprops=arrow_props)
            
            # Comparator -> Output (from center to bottom right)
            comp_to_out_dx = out_x - comp_x
            comp_to_out_dy = out_y - comp_y
            comp_to_out_dist = math.sqrt(comp_to_out_dx**2 + comp_to_out_dy**2)
            comp_start_x = comp_x + (comp_to_out_dx / comp_to_out_dist) * circle_radius
            comp_start_y = comp_y + (comp_to_out_dy / comp_to_out_dist) * circle_radius
            out_end_x = out_x - (comp_to_out_dx / comp_to_out_dist) * circle_radius
            out_end_y = out_y - (comp_to_out_dy / comp_to_out_dist) * circle_radius
            
            ax.annotate('', xy=(out_end_x, out_end_y), 
                       xytext=(comp_start_x, comp_start_y),
                       arrowprops=arrow_props)
        else:
            # Draw simple lines between circle centers
            line_props = dict(lw=unit_line_width, color='black', zorder=2)
            
            # Reference -> Comparator
            ax.plot([ref_x, comp_x], [ref_y, comp_y], **line_props)
            
            # Perception -> Comparator
            ax.plot([perc_x, comp_x], [perc_y, comp_y], **line_props)
            
            # Comparator -> Output
            ax.plot([comp_x, out_x], [comp_y, out_y], **line_props)
        
        # Store positions for inter-level connections
        unit_positions[(level, col)] = {
            'reference': (ref_x, ref_y),
            'comparator': (comp_x, comp_y),
            'output': (out_x, out_y),
            'perception': (perc_x, perc_y)
        }
    
    # Draw all units level by level
    for level in range(levels):
        num_cols = columns_per_level[level]
        y_pos = (levels - level - 1) * level_spacing
        
        # Center the columns horizontally
        if num_cols == 1:
            x_positions = [0]
        else:
            total_width = (num_cols - 1) * column_spacing
            x_positions = [-total_width/2 + i * column_spacing for i in range(num_cols)]
        
        for col, x_pos in enumerate(x_positions):
            draw_unit(x_pos, y_pos, level, col)
    
    # Draw inter-level connections
    for level in range(levels - 1):
        current_level_cols = columns_per_level[level]
        next_level_cols = columns_per_level[level + 1]
        
        # Output connections: all outputs from current level to all references in next level
        for curr_col in range(current_level_cols):
            curr_output_pos = unit_positions[(level, curr_col)]['output']
            
            for next_col in range(next_level_cols):
                next_ref_pos = unit_positions[(level + 1, next_col)]['reference']
                
                # Draw curved connection
                draw_curved_connection(ax, curr_output_pos, next_ref_pos, 
                                     color='black', style='output', use_arrows=inter_level_arrows, 
                                     unit_size=unit_size, arrow_length_factor=arrow_length_factor,
                                     curve_control_factor=curve_control_factor, 
                                     curve_line_width=curve_line_width, curve_alpha=curve_alpha,
                                     curve_resolution=curve_resolution, arrowhead_size=arrowhead_size,
                                     arrowhead_style=arrowhead_style)
        
        # Perception connections: all perceptions from next level to all perceptions in current level
        for next_col in range(next_level_cols):
            next_perc_pos = unit_positions[(level + 1, next_col)]['perception']
            
            for curr_col in range(current_level_cols):
                curr_perc_pos = unit_positions[(level, curr_col)]['perception']
                
                # Draw curved connection
                draw_curved_connection(ax, next_perc_pos, curr_perc_pos, 
                                     color='blue', style='perception', use_arrows=inter_level_arrows, 
                                     unit_size=unit_size, arrow_length_factor=arrow_length_factor,
                                     curve_control_factor=curve_control_factor,
                                     curve_line_width=curve_line_width, curve_alpha=curve_alpha,
                                     curve_resolution=curve_resolution, arrowhead_size=arrowhead_size,
                                     arrowhead_style=arrowhead_style)
    
    # Set axis limits and remove axes
    ax.set_xlim(-column_spacing * max(columns_per_level), 
                column_spacing * max(columns_per_level))
    ax.set_ylim(-level_spacing, levels * level_spacing)
    ax.axis('off')
    
    # Add title if requested
    if show_title:
        plt.title(f'PCT Hierarchy: {levels} Levels, {columns_per_level} Units per Level', 
                  fontsize=14, fontweight='bold', pad=20)
    
    # Add legend if requested
    if show_legend:
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['reference'], 
                       markersize=10, label='Reference'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['comparator'], 
                       markersize=10, label='Comparator'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['output'], 
                       markersize=10, label='Output'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['perception'], 
                       markersize=10, label='Perception')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure instead of showing it
    
    print(f"PCT Hierarchy saved as {filename}")

def draw_curved_connection(ax, start_pos, end_pos, color, style, use_arrows=True, unit_size=0.3, 
                         arrow_length_factor=0.5, curve_control_factor=0.3, curve_line_width=1.0, 
                         curve_alpha=0.7, curve_resolution=100, arrowhead_size=0.3, arrowhead_style='-|>'):
    """Draw S-curve connection between two points with proper styling and optional arrowheads"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    # Create S-curve using bezier curve with control points
    # Make the curve more pronounced for better visibility
    vertical_distance = abs(y2 - y1)
    
    # Control points create the S-shape
    # First control point - offset vertically from start point
    ctrl1_x = x1
    ctrl1_y = y1 + (y2 - y1) * curve_control_factor
    
    # Second control point - offset vertically from end point  
    ctrl2_x = x2
    ctrl2_y = y2 - (y2 - y1) * curve_control_factor
    
    # Calculate circle radius
    circle_radius = unit_size * 0.15
    
    # Adjust start and end points to be at circle edges
    # Start point adjustment
    start_dx = ctrl1_x - x1
    start_dy = ctrl1_y - y1
    start_length = math.sqrt(start_dx**2 + start_dy**2)
    if start_length > 0:
        start_dx_norm = start_dx / start_length
        start_dy_norm = start_dy / start_length
        x1_adj = x1 + start_dx_norm * circle_radius
        y1_adj = y1 + start_dy_norm * circle_radius
    else:
        x1_adj = x1
        y1_adj = y1
    
    # End point adjustment
    end_dx = x2 - ctrl2_x
    end_dy = y2 - ctrl2_y
    end_length = math.sqrt(end_dx**2 + end_dy**2)
    if end_length > 0:
        end_dx_norm = end_dx / end_length
        end_dy_norm = end_dy / end_length
        x2_adj = x2 - end_dx_norm * circle_radius
        y2_adj = y2 - end_dy_norm * circle_radius
    else:
        x2_adj = x2
        y2_adj = y2
    
    # Create bezier curve points with adjusted endpoints
    t = np.linspace(0, 1, curve_resolution)
    
    # Cubic bezier formula: P(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃
    bezier_x = (1-t)**3 * x1_adj + 3*(1-t)**2*t * ctrl1_x + 3*(1-t)*t**2 * ctrl2_x + t**3 * x2_adj
    bezier_y = (1-t)**3 * y1_adj + 3*(1-t)**2*t * ctrl1_y + 3*(1-t)*t**2 * ctrl2_y + t**3 * y2_adj
    
    # Different line styles based on connection type
    if style == 'output':
        # Output connections: solid black S-curves going downward
        # Always draw the S-curve first
        ax.plot(bezier_x, bezier_y, color='black', linewidth=curve_line_width, 
                linestyle='-', alpha=curve_alpha, zorder=1)
        
        # Add arrowhead at the end if requested
        if use_arrows:
            # Find the direction vector from second-to-last to last point of the curve
            dx = bezier_x[-1] - bezier_x[-5]  # Use more points for better direction
            dy = bezier_y[-1] - bezier_y[-5]
            length = math.sqrt(dx**2 + dy**2)
            
            if length > 0:
                dx_norm = dx / length
                dy_norm = dy / length
                
                # Create arrowhead at the end of the curve
                arrow_length = unit_size * arrow_length_factor
                arrowhead_length = unit_size * arrowhead_size
                ax.annotate('', xy=(bezier_x[-1], bezier_y[-1]), 
                           xytext=(bezier_x[-1] - dx_norm*arrow_length, bezier_y[-1] - dy_norm*arrow_length),
                           arrowprops=dict(arrowstyle=arrowhead_style, lw=1.0, alpha=1.0, 
                                         facecolor='black', edgecolor='black',
                                         mutation_scale=arrowhead_length*10))
    elif style == 'perception':
        # Perception connections: dotted blue S-curves going upward
        # Always draw the S-curve first
        ax.plot(bezier_x, bezier_y, color='blue', linewidth=curve_line_width, 
                linestyle=':', alpha=curve_alpha, zorder=1)
        
        # Add arrowhead at the end if requested
        if use_arrows:
            # Find the direction vector from second-to-last to last point of the curve
            dx = bezier_x[-1] - bezier_x[-5]  # Use more points for better direction
            dy = bezier_y[-1] - bezier_y[-5]
            length = math.sqrt(dx**2 + dy**2)
            
            if length > 0:
                dx_norm = dx / length
                dy_norm = dy / length
                
                # Create arrowhead at the end of the curve
                arrow_length = unit_size * arrow_length_factor
                arrowhead_length = unit_size * arrowhead_size
                ax.annotate('', xy=(bezier_x[-1], bezier_y[-1]), 
                           xytext=(bezier_x[-1] - dx_norm*arrow_length, bezier_y[-1] - dy_norm*arrow_length),
                           arrowprops=dict(arrowstyle=arrowhead_style, lw=1.0, alpha=1.0,
                                         facecolor='blue', edgecolor='blue',
                                         mutation_scale=arrowhead_length*10))

# Example usage
if __name__ == "__main__":
    # Create different hierarchy configurations


    draw_pct_hierarchy(levels=2, columns_per_level=[2,2], 
                      filename="pct_hierarchy_control_2x2.png", 
                      curve_control_factor=0.7, curve_line_width=0.5,
                      level_spacing=6.0)


    draw_pct_hierarchy(levels=3, columns_per_level=[4, 4, 4], 
                      filename="pct_hierarchy_control_4x4x4.png", 
                      curve_control_factor=0.7, curve_line_width=0.5,
                      level_spacing=6.0, column_spacing=4, unit_size=1.5)
    
    print("Hierarchies with different curve parameters created!")
