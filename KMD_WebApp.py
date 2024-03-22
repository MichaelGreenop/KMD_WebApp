import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use('ggplot')
from matplotlib.colors import LinearSegmentedColormap
from sklearn.cluster import KMeans
from PIL import Image
from io import BytesIO
from renishawWiRE import WDFReader


# Tasks - General functions section



def cluster_select(original_df, cluster):
    # Create a copy of the original DataFrame
    df_copy = original_df.copy()

    # Set all values in rows not related to the specified index to zero
    df_copy.loc[df_copy.index != cluster, :] = 0

    return df_copy

def select_range(input_df, start_column, end_column):
    # Convert column labels to a list for validation
    column_labels = list(input_df.columns)

    # Check if start and end columns are valid
    if start_column not in column_labels or end_column not in column_labels:
        st.error("Please enter valid column labels.")
        return None

    # Select a range of columns based on the start and end column labels
    selected_columns = input_df.loc[:, start_column:end_column]

    return selected_columns
      




def home_page():
    
    # Tasks     

    st.markdown("Home page")
    st.sidebar.markdown("Home page")

    st.write("""
    The aim of this app is to provide a method of objectively\n
    choosing shading boundaries within vibrational spectroscopy\n
    images using k-means clustering
    \n
    Index:\n
        Page 1: Investigate individual clusters\n
        Page 2: Compare clusters\n
        Page 3: Produce layers\n
        Page 4: Combine layers\n
        Page 5: Add colour ranges\n
             """)
        

    


def page1():
    st.markdown("Page 1: Investigate individual clusters")
    st.sidebar.markdown("Page 1: Investigate individual clusters")
    
    st.write('''Observe the average spectrum for a specific cluster and alter the number of clusters.''')

    

    # File Upload
    uploaded_file = st.file_uploader("Upload WDF File", type=["wdf"])

    if uploaded_file is not None:
        st.write("Uploaded file:", uploaded_file.name)

        try:
            # Read WDF file
            with open(uploaded_file.name, 'wb') as f:
                f.write(uploaded_file.read())
            reader = WDFReader(uploaded_file.name)

            # Get spectra and data matrix shape
            spectra = reader.spectra
            shp = spectra.shape

            # Convert spectra to a NumPy array and reshape
            data_matrix = spectra.reshape((shp[0] * shp[1], shp[2]))

            # Get wavenumber range
            wn = reader.xdata

            # User input for the number of clusters
            num_clusters = st.slider("Select the number of clusters:", min_value=2, max_value=10, value=4)

            # Perform KMeans clustering
            kmeans = KMeans(n_clusters=num_clusters, random_state=0)
            clusters = kmeans.fit_predict(data_matrix)

            # Convert wn and spectra to DataFrames
            wn_df = pd.DataFrame(wn, columns=['labels'])
            spectra_df = pd.DataFrame(data_matrix, columns=[f'spectra_{i}' for i in range(shp[2])])

            # Convert clusters to a NumPy array and reshape
            clusters_array = clusters.reshape((shp[0], shp[1]))

            # User input for selected cluster
            selected_cluster = st.number_input("Enter the cluster number to highlight:", min_value=0, max_value=num_clusters-1, value=0)

            # Check if the input is valid
            if selected_cluster not in range(num_clusters):
                st.error("Please enter a valid cluster number.")

            # Plot the clusters array using plt.imshow()
            fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 5))

            # Plot clusters_array
            ax0.imshow(np.where(clusters_array == selected_cluster, 1, 0), cmap='Reds', interpolation='nearest', aspect='auto')
            ax0.set_xlabel('x-length (μm)')
            ax0.set_ylabel('y-length (μm)')
            ax0.set_title('K-means map', fontsize=10)
            ax0.grid(False)

            # Extract rows associated with the selected cluster
            selected_rows = spectra_df.loc[clusters == selected_cluster]

            # Plot the average of the selected rows
            ax1.plot(wn, selected_rows.mean(axis=0), label=f'Cluster {selected_cluster}', color='red')
            ax1.set_xlabel('Wavenumber')
            ax1.set_ylabel('Average Intensity')
            ax1.set_title('Average Spectrum for Selected Cluster', fontsize=10)
            ax1.legend()
            ax1.grid(True)

            st.write(fig)
            

        except Exception as e:
            st.error(f"Error reading the WDF file: {e}")


def page2():


    # Tasks:
    
    st.markdown("Page 2: Compare clusters)")
    st.sidebar.markdown("Page 2: Compare clusters")

    st.write("""See all the clusters in a single map, alter the cluster numbers to compare their average spectra
   
    """)

    # File Upload
    uploaded_file = st.file_uploader("Upload WDF File", type=["wdf"])

    if uploaded_file is not None:
        st.write("Uploaded file:", uploaded_file.name)

        try:
            # Read WDF file
            with open(uploaded_file.name, 'wb') as f:
                f.write(uploaded_file.read())
            reader = WDFReader(uploaded_file.name)

            # Get spectra and data matrix shape
            spectra = reader.spectra
            shp = spectra.shape

            # Convert spectra to a NumPy array and reshape
            data_matrix = spectra.reshape((shp[0] * shp[1], shp[2]))

            # Get wavenumber range
            wn = reader.xdata

            # User input for the number of clusters
            num_clusters = st.slider("Select the number of clusters:", min_value=2, max_value=10, value=4)

            # Perform KMeans clustering
            kmeans = KMeans(n_clusters=num_clusters, random_state=0)
            clusters = kmeans.fit_predict(data_matrix)

            # Convert wn and spectra to DataFrames
            wn_df = pd.DataFrame(wn, columns=['labels'])
            spectra_df = pd.DataFrame(data_matrix, columns=[f'spectra_{i}' for i in range(shp[2])])

            # Convert clusters to a NumPy array and reshape
            clusters_array = clusters.reshape((shp[0], shp[1]))

            # User input for selected cluster
            selected_cluster = st.number_input("Enter the cluster number to highlight:", min_value=0, max_value=num_clusters-1, value=0)

            # Check if the input is valid
            if selected_cluster not in range(num_clusters):
                st.error("Please enter a valid cluster number.")

            # Second cluster input
            
            selected_cluster2 = st.number_input("Enter a second cluster number to highlight:", min_value=0, max_value=num_clusters-1, value=0)
            if selected_cluster2 not in range(num_clusters):
                st.error("Please enter a valid cluster number.")

            # Plot the clusters array using plt.imshow()
            fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(15, 5))
            

            # Plot clusters_array
            cax = ax0.imshow(clusters_array, aspect='equal')
            ax0.set_xlabel('x-length (μm)')
            ax0.set_ylabel('y-length (μm)')
            ax0.set_title('K-means map (All Clusters)', fontsize=10)
            fig.colorbar(cax, ax=ax0, orientation='vertical', fraction=0.046, pad=0.04)
            ax0.grid(False)

            # Extract rows associated with the selected cluster
            selected_rows = spectra_df.loc[clusters == selected_cluster]
            selected_rows2 = spectra_df.loc[clusters == selected_cluster2]

            # Plot the average of the selected rows
            ax1.plot(wn, selected_rows.mean(axis=0), label=f'Cluster {selected_cluster}', color='red')
            ax1.plot(wn, selected_rows2.mean(axis=0), label=f'Cluster {selected_cluster2}', color='blue')
            ax1.set_xlabel('Wavenumber')
            ax1.set_ylabel('Average Intensity')
            ax1.set_title('Cluster Average Spectrum Compare', fontsize=10)
            ax1.legend()
            ax1.grid(True)

            st.write(fig)
            

        except Exception as e:
            st.error(f"Error reading the WDF file: {e}")


def page3():

    st.markdown("Page 3: Produce layers)")
    st.sidebar.markdown("Page 3: Produce layers")

    st.write("""
    On this page, layers are prodcuced, relating to a single cluster, linking a \n 
    spectral feature to the cluster.\n THe spectral feature intensity relating to colour intentisy). 
    """)



    #Start = ''
    #End = ''

    Start = st.text_input("Range start: ")
    End = st.text_input("Range end: ")


    if len(Start) is not None:
        if len(End) is not None:
            uploaded_file = st.file_uploader("Upload WDF File", type=["wdf"])

            #st.write("Uploaded file:", uploaded_file.name)
            if uploaded_file is not None:
                
                try:
                # Read WDF file
                    with open(uploaded_file.name, 'wb') as f:
                        f.write(uploaded_file.read())
                        reader = WDFReader(uploaded_file.name)

                        # Get spectra and data matrix shape
                        spectra = reader.spectra
                        shp = spectra.shape

                        # Convert spectra to a NumPy array and reshape
                        data_matrix = spectra.reshape((shp[0] * shp[1], shp[2]))

                        # Get wavenumber range
                        w = reader.xdata
                        wn = w.astype(float).astype(int)

                        # User input for the number of clusters
                        num_clusters = st.slider("Select the number of clusters:", min_value=2, max_value=10)
                
                        if num_clusters is not None:
                            # Perform KMeans clustering
                            kmeans = KMeans(n_clusters=num_clusters, random_state=0)
                            clusters = kmeans.fit_predict(data_matrix)

                            Clusters = pd.DataFrame(clusters).rename(columns={0:'labels'})

                            # Convert wn and spectra to DataFrames
                            spectra_df = pd.DataFrame(data_matrix, columns=wn)
                            df = pd.concat([Clusters, spectra_df], axis=1).set_index(['labels'])

                             # User input for selected cluster
                            selected_cluster = st.number_input("Enter the cluster number to highlight:", min_value=0, max_value=num_clusters-1, value=0)
                            #colour = st.text_input("Colour: ")

                            # Check if the input is valid
                            if selected_cluster not in range(num_clusters):
                                st.error("Please enter a valid cluster number.")
                            else:
                                df1 = cluster_select(df, selected_cluster)
                      
                                df2 = select_range(df1, int(End), int(Start))
                           

                                st.write(df2.head(2))

                                img_array = df2.values.mean(axis=1)

                                img = img_array.reshape((shp[0],shp[1]))


                                
                                colors_g = [(0, 0, 0), (0, 1, 0)]  # Green -> Black
                                cmap_name_g = 'my_list'
                                cmap_gb = LinearSegmentedColormap.from_list(cmap_name_g, colors_g, N=30)
                                
                                colors_r = [(0, 0, 0), (1, 0, 0)]  # Red -> Black
                                cmap_name_r = 'my_list'
                                cmap_rb = LinearSegmentedColormap.from_list(cmap_name_r, colors_r, N=30)

                                colors_b = [(0, 0, 0), (0, 0, 1)]  # Blue -> Black
                                cmap_name_b = 'my_list'
                                cmap_bb = LinearSegmentedColormap.from_list(cmap_name_b, colors_b, N=30)

                                colors_p = [(0, 0, 0), (0.7, 0, 0.7)]  # Purple -> Black
                                cmap_name_p = 'my_list'
                                cmap_pb = LinearSegmentedColormap.from_list(cmap_name_p, colors_p, N=30)

                                # Dropdown menu with four color options
                                selected_color = st.selectbox("Select a color:", ["Green", "Red", "Blue", "Purple"])

                                # Create a dictionary mapping color names to their corresponding cmap
                                cmap_mapping = {
                                "Green": cmap_gb,
                                "Red": cmap_rb,
                                "Blue": cmap_bb,
                                "Purple": cmap_pb
                                }

                                # Get the selected colormap
                                selected_cmap = cmap_mapping.get(selected_color, plt.cm.Greens)


                                # Plot the clusters array using plt.imshow()
                                from mpl_toolkits.axes_grid1 import make_axes_locatable
                                
                                fig, ax0 = plt.subplots(figsize=(8, 6))
                                divider = make_axes_locatable(ax0)
                                cax = divider.append_axes('right', size='5%', pad=0.05)

                                # Plot clusters_array with colorbar
                                im = ax0.imshow(img, cmap=selected_cmap, interpolation='bicubic', aspect='auto')
                                ax0.grid(False)
                                ax0.axes.xaxis.set_visible(False)
                                ax0.axes.yaxis.set_visible(False)
                                fig.colorbar(im, cax=cax, orientation='vertical')
                                

                                st.write(fig)


                                # Save the figure to a file
                                name = st.text_input("Enter the filename (with extension):")
                                #save_button = st.button("Save Figure")


                                def download_button(plot, filename, button_text='Download Plot'):
                                    # Save the plot to a BytesIO buffer
                                    buf = BytesIO()
                                    plot.savefig(buf, format='png')
                                    buf.seek(0)

                                    # Create a download button
                                    st.download_button(label=button_text, data=buf, file_name=filename, key='download_button')

                             

                                
       

                                if len(name) > 0: 

                                    # Call the download_button function
                                    download_button(fig, name)
                                                                      
                                    st.success(f"Press the download button to save: {name}")

                except Exception as e:
                    st.error(f"Error reading the WDF file: {e}")
             



def page4():

    # Tasks:

    st.markdown("Page 4: Combine layers")
    st.sidebar.markdown("Page 4: Combine layers")

    st.write("""
    The layers produced on the previous page can now be combined.\n
    
    If there are more than two layers, repeat the process on the first combined map. 
    """)
    # Upload the first PNG image
    uploaded_image1 = st.file_uploader("Choose the first PNG image", type=["png"])

    # Upload the second PNG image
    uploaded_image2 = st.file_uploader("Choose the second PNG image", type=["png"])

    # Save the figure to a file
    name1 = st.text_input("Enter the filename (with extension):")

    # Button to make black pixels in the first image transparent
    make_transparent_button = st.button("Combine the images")

    

    # Check if both images are uploaded and the button is pressed
    if uploaded_image1 is not None and uploaded_image2 is not None and make_transparent_button is not None and len(name1) > 0:
        # Convert the uploaded images to PIL Images
        pil_image1 = Image.open(uploaded_image1).crop((101, 53, 687, 550))
        pil_image2 = Image.open(uploaded_image2).crop((101, 53, 687, 550))



        # Function to make black pixels transparent
        def make_black_pixels_transparent(input_image):
            # Convert the image to RGBA mode
            image_rgba = input_image.convert('RGBA')

            # Get pixel data
            pixeldata = list(image_rgba.getdata())

            # Make all black pixels transparent
            for i, pixel in enumerate(pixeldata):
                if pixel[:3] == (0, 0, 0):
                    pixeldata[i] = (0, 0, 0, 0)  # Set alpha to 0 for black pixels

            # Update the image with the modified pixel data
            image_rgba.putdata(pixeldata)

            return image_rgba

        # Apply the function to the first image
        transparent_image1 = make_black_pixels_transparent(pil_image1)



        def combine_images(background, foreground):
            # Create a copy of the background image to avoid modifying the original
            combined_image = background.copy()

            # Paste the foreground image onto the combined image
            combined_image.paste(foreground, (0, 0), foreground)

            return combined_image

        # Overlay the transparent image on top of the non-transparent image
        final_image = combine_images(pil_image2, transparent_image1)



        # Display the final image
        st.image([final_image], 
                caption=["Combined Img"],
                use_column_width=True)

    
        def download_button2(plot1, filename1, button_text='Download Plot'):
            # Save the plot to a BytesIO buffer
            buf1 = BytesIO()
            plot1.save(buf1, 'png')
            buf1.seek(0)

                                    # Create a download button
            st.download_button(label=button_text, data=buf1, file_name=filename1, key='download_button')
                
 
            

        download_button2(final_image, name1)
        st.success(f"Press the download button to save: {name1}")
            

def page5():


    st.markdown("Page 5: Add colour ranges")
    st.sidebar.markdown("Page 5: Add colour ranges")

    st.write("""
    The combined map produced on the previous page now requires the \n
    colour ranges to be added. 
    """)
    # Upload the first PNG image
    uploaded_image3 = st.file_uploader("Choose map (PNG format)", type=["png"])

    # Upload the second PNG image
    uploaded_image4 = st.file_uploader("Choose the first colour range (PNG format)", type=["png"])

    # Upload the second PNG image
    uploaded_image5 = st.file_uploader("Choose the second colour range (PNG format)", type=["png"])

    # Upload the second PNG image
    uploaded_image6 = st.file_uploader("Choose the third colour range (PNG format)", type=["png"])

    # Button to make black pixels in the first image transparent
    combine_button = st.button("Create final figure")


 

    # Check if both images are uploaded and the button is pressed
    if uploaded_image3 is not None and uploaded_image4 is not None and uploaded_image5 is not None and uploaded_image6 is not None and combine_button:
        # Convert the uploaded images to PIL Images
        pil_image3 = Image.open(uploaded_image3).crop((1, 33, 585, 480))
        pil_image4 = Image.open(uploaded_image4).crop((687, 53, 780, 550))
        pil_image5 = Image.open(uploaded_image5).crop((687, 53, 780, 550))
        pil_image6 = Image.open(uploaded_image6).crop((687, 53, 780, 550))

        def combine_images(image1, image2, image3, image4):
            # Get the sizes of each image
            width3, height3 = pil_image3.size
            width4, height4 = pil_image4.size
            width5, height5 = pil_image5.size
            width6, height6 = pil_image6.size

            # Determine the size of the combined image
            combined_width = width3 + width4 + width5 + width6 
            combined_height = height4

            # Create a new image with the determined size
            combined_image = Image.new('RGB', (combined_width, combined_height))

            # Paste each image onto the combined image
            combined_image.paste(pil_image3, (0,0))
            combined_image.paste(pil_image4, (width3 , 0))
            combined_image.paste(pil_image5, (width3 + width4, 0))
            combined_image.paste(pil_image6, (width3 + width4 + width5, 0))
            
            return combined_image


        final_image2 = combine_images(pil_image3, pil_image4, pil_image5, pil_image6)

        # Display the final image
        st.image([final_image2], 
                caption=["Final Img"],
                use_column_width=True)


       
        # Save the figure to a file
        name2 = st.text_input("Enter the filename (with extension):")
        #save_button = st.button("Save Figure")
                                
       

        def download_button3(plot2, filename2, button_text='Download Plot'):
            # Save the plot to a BytesIO buffer
            buf2 = BytesIO()
            plot2.save(buf2, 'png')
            buf2.seek(0)

            # Create a download button
            st.download_button(label=button_text, data=buf2, file_name=filename2, key='download_button')
                
 
            

        download_button3(final_image2, name2)
        st.success(f"Press the download button to save: {name2}")

             
                
        

        

        


page_names_to_funcs = {  



    "Home Page": home_page,
    "Page 1: Investigate individual clusters": page1,
    "Page 2: Compare clusters": page2, 
    "Page 3: Produce layers": page3,
    "Page 4: Combine layers": page4,
    "Page 5: Add colour ranges": page5,
    }

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
