import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Function to load and process the file
def load_file(file):
    if file.type == 'text/csv':
        return pd.read_csv(file)
    elif file.type == 'text/plain':
        delimiter = st.sidebar.text_input("Enter the delimiter used in the TXT file (e.g., ',' for CSV, '\\t' for tab):", value=",")
        return pd.read_csv(file, sep=delimiter)
    elif file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return pd.read_excel(file, sheet_name=None)  # Returns a dictionary of DataFrames
    else:
        st.error("Unsupported file type")
        return None

# Function to download plot
def download_plot(fig, format='png'):
    buf = BytesIO()
    fig.savefig(buf, format=format)
    return buf

# Function to provide a description of the chart based on user's selection
def chart_description(chart_type, analysis_type):
    descriptions = {
        "Histogram": (
            "A histogram is used to visualize the distribution of a single continuous numerical variable. "
            "**Variable Type:** Continuous or discrete numerical variables."
        ),
        "Box Plot": (
            "A box plot displays the distribution of a numerical variable and identifies outliers. "
            "**Variable Type:** Continuous numerical variables."
        ),
        "Density Plot (KDE)": (
            "A density plot estimates the probability density function of a continuous variable. "
            "**Variable Type:** Continuous numerical variables."
        ),
        "Bar Chart": (
            "A bar chart shows the frequency or proportion of categories for categorical variables. "
            "**Variable Type:** Categorical variables."
        ),
        "Pie Chart": (
            "A pie chart represents the relative proportions of categories in a dataset. "
            "**Variable Type:** Categorical variables."
        ),
        "Violin Plot": (
            "A violin plot combines aspects of a box plot and density plot to show the distribution of the data. "
            "**Variable Type:** Continuous numerical variables."
        ),
        "Scatter Plot": (
            "A scatter plot shows the relationship between two continuous numerical variables. "
            "**Variable Type:** Two continuous numerical variables."
        ),
        "Line Plot": (
            "A line plot visualizes trends over time for continuous numerical variables. "
            "**Variable Type:** Two continuous numerical variables, often time-series data."
        ),
        "Lollipop Chart": (
            "A lollipop chart is used to compare a single numerical value across different categories, "
            "where each data point is represented by a line connecting a category to its value. "
            "**Variable Type:** Categorical (x-axis) and continuous numerical variables (y-axis)."
        ),
    }

    return descriptions.get(chart_type, f"{analysis_type} chart selected. No specific description available.")

# Custom CSS for styling the multiselect dropdown, navigation buttons, and footer
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }
        .stApp {
            background: #f5f5f5;
        }
        .sidebar .sidebar-content {
            background-color: #3E4E88;
            color: white;
        }
        .sidebar .sidebar-content a {
            color: white;
            font-weight: bold;
        }
        .sidebar .sidebar-content a:hover {
            color: #FFD700;
        }
        .reportview-container .main .block-container {
            padding-top: 2rem;
            padding-bottom: 4rem;  /* Make space for the footer */
        }
        h1, h2, h3 {
            color: #3E4E88;
        }
        h4 {
            color: #FFD700;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #3E4E88;
            color: white;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            height: 60px; /* Set a fixed height for the footer */
            z-index: 100;
        }
        .footer a {
            color: white;
            margin: 0 10px;
            text-decoration: none;
        }
        .footer a:hover {
            color: #FFD700;
        }
        .footer-text {
            margin-top: 5px;
            font-size: 12px;
            color: #FFD700;
        }
        .footer-icons {
            font-size: 18px;
        }
        /* Custom styles for the navigation tiles */
        .nav-button {
            display: block;
            background-color: #3E4E88;
            color: white;
            padding: 15px;
            margin-bottom: 10px;
            text-align: center;
            border-radius: 10px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s, background-color 0.3s;
            text-decoration: none;
            font-size: 18px;
        }
        .nav-button:hover {
            transform: scale(1.05);
            background-color: #FFD700;
            color: #3E4E88;
            cursor: pointer;
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3);
        }
        /* Custom CSS for the multiselect dropdown */
        div[data-baseweb="select"] > div {
            background-color: lightcoral !important;
            color: white !important;
        }
        div[data-baseweb="select"] > div:hover {
            background-color: red !important;
            color: white !important;
        }
        div[data-baseweb="select"] > div:focus-within {
            background-color: red !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation with styled buttons
st.sidebar.title("Navigation")

if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("About Us"):
    st.session_state.page = "About Us"
if st.sidebar.button("Visualization"):
    st.session_state.page = "Visualization"

# Set the default page if none is selected
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Function to toggle label orientation
def toggle_orientation(ax, axis, orientation):
    if axis == 'x':
        ax.tick_params(axis='x', rotation=orientation)
    elif axis == 'y':
        ax.tick_params(axis='y', rotation=orientation)

# Home page content
if st.session_state.page == "Home":
    st.title("Welcome to the Data Visualization Project")
    st.markdown("""
    ### Your Data, Beautifully Visualized

    **Transform your data into impactful insights!**

    This application allows you to upload data files and perform various types of visualizations with ease.

    #### Instructions:
    - Use the sidebar to upload your data file.
    - Choose the type of analysis and plot you want to create.
    - Download your plot in different formats.

    #### Features:
    - Support for CSV, TXT, and XLSX files.
    - Multiple types of plots for univariate, bivariate, and multivariate analysis.

    """)
    st.image("./HomePageImage.jpg", use_column_width=True)

# About Us page content
elif st.session_state.page == "About Us":
    st.title("About Us")
    st.markdown("""
    ## About Data Visualization Project

    **Empowering Your Data Journey with Expertise and Precision.**

    Our mission is to make data analysis accessible and visually appealing for everyone, from beginners to experts.

    #### Meet the Team:
    - **Muhammad Nadeem**: Data Scientist - Passionate about transforming complex datasets into actionable insights and driving data-driven decision-making.
    - **Mehar Hamid Ishfaq**: Data Analyst - Expert in analyzing data trends and creating seamless user experiences through data-driven solutions.
    - **Muhammad Bilal Butt**: UI/UX Designer - Focused on integrating data science with user experience to make data insights both beautiful and accessible.

    ### Contact Us:
    Have questions? Feel free to reach out to us at [mr.nadeempredictermodeler@gmail.com](mailto:support@datavisualization.com).

    """)
    st.image("./AboutUsPage.jpg", use_column_width=True)

# Visualization page content
elif st.session_state.page == "Visualization":
    st.title("Data Visualization")

    st.sidebar.header("Upload Data File")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "txt", "xlsx"])

    if uploaded_file is not None:
        data = load_file(uploaded_file)

        if isinstance(data, dict):  # XLSX with multiple sheets
            sheet = st.sidebar.selectbox("Select a sheet", data.keys())
            df = data[sheet]
        else:
            df = data

        if df is not None:
            st.markdown("### Data Preview")
            st.dataframe(df.head(), height=200)

            # Statistical Analysis
            st.sidebar.header("Statistical Analysis")
            stat_option = st.sidebar.selectbox("Select a Statistical Function", ["Describe", "Correlation", "Value Counts"])

            if stat_option == "Describe":
                st.markdown("### Descriptive Statistics")
                st.write(df.describe())
            elif stat_option == "Correlation":
                st.markdown("### Correlation Matrix")
                st.write(df.corr())
            elif stat_option == "Value Counts":
                column = st.sidebar.selectbox("Select Column for Value Counts", df.columns)
                st.markdown(f"### Value Counts for {column}")
                st.write(df[column].value_counts())

            # Data selection
            if st.sidebar.checkbox("Select specific columns"):
                columns = st.sidebar.multiselect("Select columns", df.columns)
                if columns:
                    df = df[columns]

            # Analysis type selection
            st.sidebar.header("Plot Configuration")
            analysis_type = st.sidebar.selectbox("Select Analysis Type", ["Univariate", "Bivariate", "Multivariate"])

            # Variables to track label orientation
            x_label_orientation = 0
            y_label_orientation = 0

            # Plot suggestion and generation
            if analysis_type == "Univariate":
                plot_type = st.sidebar.selectbox("Select plot type", ["Histogram", "Box Plot", "Density Plot (KDE)", "Bar Chart", "Pie Chart", "Violin Plot", "Lollipop Chart"])
                selected_column = st.sidebar.selectbox("Select column", df.columns)
                st.markdown(f"**Description:** {chart_description(plot_type, analysis_type)}")

                fig, ax = plt.subplots()
                if plot_type == "Histogram":
                    sns.histplot(df[selected_column], ax=ax, color="#3E4E88")
                elif plot_type == "Box Plot":
                    sns.boxplot(data=df[selected_column], ax=ax, color="#3E4E88")
                elif plot_type == "Density Plot (KDE)":
                    sns.kdeplot(df[selected_column], ax=ax, color="#3E4E88")
                elif plot_type == "Bar Chart":
                    sns.countplot(x=df[selected_column], ax=ax, color="#3E4E88")
                elif plot_type == "Pie Chart":
                    df[selected_column].value_counts().plot.pie(autopct='%1.1f%%', ax=ax, colors=sns.color_palette("coolwarm", len(df[selected_column].unique())))
                    ax.set_ylabel('')
                elif plot_type == "Violin Plot":
                    sns.violinplot(data=df[selected_column], ax=ax, color="#3E4E88")
                elif plot_type == "Lollipop Chart":
                    sns.scatterplot(x=df[selected_column], y=df.index, ax=ax, color="#3E4E88", marker='o', s=100)
                    ax.vlines(x=df[selected_column], ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], colors="#3E4E88", linestyles="solid")

                # Toggle buttons for x-axis and y-axis label orientation
                if st.button("Toggle X-axis Labels"):
                    x_label_orientation = 90 if x_label_orientation == 0 else 0
                    toggle_orientation(ax, 'x', x_label_orientation)
                    st.pyplot(fig)

                if st.button("Toggle Y-axis Labels"):
                    y_label_orientation = 90 if y_label_orientation == 0 else 0
                    toggle_orientation(ax, 'y', y_label_orientation)
                    st.pyplot(fig)

                st.pyplot(fig)

                # Button to download the modified graph
                st.sidebar.header("Download Plot")
                download_format = st.sidebar.selectbox("Select format", ["PNG", "JPEG", "PDF"])
                if st.sidebar.button("Download Plot"):
                    buf = download_plot(fig, format=download_format.lower())
                    st.sidebar.download_button(label="Download Plot", data=buf, file_name=f"plot.{download_format.lower()}")

            elif analysis_type == "Bivariate":
                plot_type = st.sidebar.selectbox("Select plot type", ["Scatter Plot", "Line Plot", "Box Plot", "Violin Plot"])
                x_col = st.sidebar.selectbox("Select X-axis", df.columns)
                y_col = st.sidebar.selectbox("Select Y-axis", df.columns)
                st.markdown(f"**Description:** {chart_description(plot_type, analysis_type)}")

                fig, ax = plt.subplots()
                if plot_type == "Scatter Plot":
                    sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax, color="#3E4E88")
                elif plot_type == "Line Plot":
                    sns.lineplot(x=df[x_col], y=df[y_col], ax=ax, color="#3E4E88")
                elif plot_type == "Box Plot":
                    sns.boxplot(x=df[x_col], y=df[y_col], ax=ax, color="#3E4E88")
                elif plot_type == "Violin Plot":
                    sns.violinplot(x=df[x_col], y=df[y_col], ax=ax, color="#3E4E88")

                # Toggle buttons for x-axis and y-axis label orientation
                if st.button("Toggle X-axis Labels"):
                    x_label_orientation = 90 if x_label_orientation == 0 else 0
                    toggle_orientation(ax, 'x', x_label_orientation)
                    st.pyplot(fig)

                if st.button("Toggle Y-axis Labels"):
                    y_label_orientation = 90 if y_label_orientation == 0 else 0
                    toggle_orientation(ax, 'y', y_label_orientation)
                    st.pyplot(fig)

                st.pyplot(fig)

                # Button to download the modified graph
                st.sidebar.header("Download Plot")
                download_format = st.sidebar.selectbox("Select format", ["PNG", "JPEG", "PDF"])
                if st.sidebar.button("Download  Plot"):
                    buf = download_plot(fig, format=download_format.lower())
                    st.sidebar.download_button(label="Download Plot", data=buf, file_name=f"plot.{download_format.lower()}")

            elif analysis_type == "Multivariate":
                plot_type = st.sidebar.selectbox("Select plot type", ["Pair Plot", "Heatmap", "3D Scatter Plot", "Parallel Coordinates Plot", "Radial Plot (Spider Plot)", "PCA Biplot"])
                st.markdown(f"**Description:** {chart_description(plot_type, analysis_type)}")

                fig, ax = plt.subplots()
                if plot_type == "Pair Plot":
                    fig = sns.pairplot(df, diag_kind="kde", plot_kws={"color": "#3E4E88"})
                elif plot_type == "Heatmap":
                    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
                elif plot_type == "3D Scatter Plot":
                    st.warning("3D Scatter Plot visualization not supported in current Streamlit version.")
                elif plot_type == "Parallel Coordinates Plot":
                    st.warning("Parallel Coordinates Plot visualization not supported in current Streamlit version.")
                elif plot_type == "Radial Plot (Spider Plot)":
                    st.warning("Radial Plot (Spider Plot) visualization not supported in current Streamlit version.")
                elif plot_type == "PCA Biplot":
                    st.warning("PCA Biplot visualization not supported in current Streamlit version.")

                if plot_type in ["Heatmap", "3D Scatter Plot"]:
                    # Toggle buttons for x-axis and y-axis label orientation
                    if st.button("Toggle X-axis Labels"):
                        x_label_orientation = 90 if x_label_orientation == 0 else 0
                        toggle_orientation(ax, 'x', x_label_orientation)
                        st.pyplot(fig)

                    if st.button("Toggle Y-axis Labels"):
                        y_label_orientation = 90 if y_label_orientation == 0 else 0
                        toggle_orientation(ax, 'y', y_label_orientation)
                        st.pyplot(fig)

                st.pyplot(fig)

                # Button to download the modified graph
                st.sidebar.header("Download Plot")
                download_format = st.sidebar.selectbox("Select format", ["PNG", "JPEG", "PDF"])
                if st.sidebar.button("Download Plot"):
                    buf = download_plot(fig, format=download_format.lower())
                    st.sidebar.download_button(label="Download Plot", data=buf, file_name=f"plot.{download_format.lower()}")

    else:
        st.info("Please upload a data file to get started.")

# Footer
st.markdown("""
    <div class="footer">
        &copy; 2024 Muhammad Nadeem. All rights reserved.
        <div class="footer-icons">
            <a href="https://www.linkedin.com/in/muhammad-nadeem-5a1517242" target="_blank"><i class="fab fa-linkedin"></i></a>
            <a href="https://github.com/NadeemMughal" target="_blank"><i class="fab fa-github"></i></a>
        </div>
        <div class="footer-text">
            Connect with us on LinkedIn and GitHub!
        </div>
    </div>
    """, unsafe_allow_html=True)

# Load FontAwesome for icons
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    """, unsafe_allow_html=True)
