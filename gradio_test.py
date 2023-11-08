import gradio as gr
import matplotlib.pyplot as plt
from io import BytesIO

def plot_function(some_input):
    # Create a plot using Matplotlib
    plt.figure()
    plt.plot([0, 1, 2], [0, some_input, some_input ** 2])
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sample Plot')

    # Save it to a bytes buffer instead of a file
    # buf = BytesIO()
    # plt.savefig(buf, format='png')
    # # Use 'buf.getvalue()' to get the byte value of the image
    # buf.seek(0)  # Need to seek back to the beginning of the BytesIO object before reading it

    # plt.close()  # Close the figure after saving to buffer

    return plt  # Return the buffer

# Create the Gradio interface
iface = gr.Interface(
    fn=plot_function,
    inputs=gr.Slider(minimum=0, maximum=10),  # for example, a slider input
    outputs=gr.Plot(),  # specify the output is an image of a plot
)

# Launch the application
iface.launch()
