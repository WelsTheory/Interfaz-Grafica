import sys 
import csv
from serial import Serial
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.widgets import Button

if sys.platform.startswith('linux'):
    port = '/dev/ttyACM0'
elif sys.platform.startswith('win'):
    port = 'COM4'
else:
    raise EnvironmentError("Este sistema operativo no es compatible")

ser = Serial(port,115200)

plt.ion()
fig, ax = plt.subplots(figsize = (10,5))
fig.patch.set_facecolor('#f0f0f0')
ax.set_title('Interfaz de ADC', fontsize = 16, color = '#333')
ax.set_xlabel('Tiempo', fontsize = 14, color = '#555')
ax.set_ylabel('Valor del ADC', fontsize = 14, color = '#555')
ax.set_ylim(0,4095)

line_color = '#1f77b4'
line, = ax.plot([],[],color = line_color, linewidth = 2, marker = 's', markersize = 4, linestyle = 'solid',label='Interfaz ADC' )
ax.legend(loc = 'upper left')

ax.grid(color = 'gray', linestyle ='--', linewidth = 0.5, alpha = 0.7)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M_%S'))
ax.xaxis.set_major_locator(mdates.SecondLocator(interval= 1))

x,y = [], []

# Archivo CSV
csv_filename = 'data_adc.csv'

def save_data(event):
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Tiempo','Valor ADC'])
        for t, v in zip(x,y):
            csv_writer.writerow([t.strftime('%H:%M_%S'),v])
    print("Datos guardados en el archivo CSV")
    
#crear boton
ax_button = plt.axes([0.8, 0.02, 0.1, 0.05])
button = Button(ax_button,'Guardar Data')
button.on_clicked(save_data)

while True:
    try:
        data = ser.readline().decode().strip()
        cleaned_data = data.replace('\x00','').replace('\r','')
        if cleaned_data.isdigit():
            adc_data = int(cleaned_data)
            current_time = datetime.now()
            print(f"Tiempo: {current_time}, Valor ADC: {adc_data}")
            x.append(current_time)
            y.append(adc_data)
            line.set_data(x,y)
            ax.relim()
            ax.autoscale_view(True,True,True)
            fig.canvas.draw()
            fig.canvas.flush_events()
        else:
            continue
    except KeyboardInterrupt:
        ser.close()
        break
    except ValueError:
        continue
