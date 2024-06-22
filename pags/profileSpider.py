import streamlit as st 
from db_connection import connect_to_db
import pandas as pd

def display_dataframe_with_links(df):
    # Display DataFrame without the 'url' column
    st.write(df.drop(columns=['url']))

    # Display 'url' column as clickable links
    for index, row in df.iterrows():
        st.markdown(f"[Link {index}]({row['url']})")

def fetch_profile_names(username_requester):
    db = connect_to_db("DiscoData")
    if db is not None:
        profilerSpider = db.ProfileSpider
        distinct_profiles = profilerSpider.distinct('profile_name', {'username_requester': username_requester})
        return distinct_profiles

def fetch_data(profile_name, username_requester):
    db = connect_to_db("DiscoData")
    if db is not None:
        profilerSpider = db.ProfileSpider
        logs = profilerSpider.find({'profile_name': profile_name, 'username_requester': username_requester}, {'_id': 0, 'profile_name': 0, 'username_requester': 0})
        return logs

def filter_data(df, for_sale_threshold, have_threshold, want_threshold):
    filtered_df = df[df['have'] <= have_threshold]
    filtered_df = filtered_df[filtered_df['want'] <= want_threshold]
    filtered_df = filtered_df[filtered_df['for_sale'] <= for_sale_threshold]
    return filtered_df

def app():
    st.header("Profile Spider Search")
    st.subheader('Filter Data Options')
    profile_names = fetch_profile_names(st.secrets["USER_REQUESTER"])
    selected_profile = st.selectbox('Select Profile Name', profile_names)
    have_threshold = st.slider("Select threshold for 'have'", min_value=0, max_value=400, value=100)
    want_threshold = st.slider("Select threshold for 'want'", min_value=0, max_value=400, value=100)
    for_sale_threshold = st.slider("Select threshold for 'for sale'", min_value=0, max_value=100, value=2)

    filter_button = st.button('Filter Data')

    if filter_button:
        data = fetch_data(selected_profile, st.secrets["USER_REQUESTER"])

        if data:
            data_list = list(data)
            df = pd.DataFrame(data_list)

            if not df.empty:
                df['have'] = pd.to_numeric(df['have'], errors='coerce')
                df['want'] = pd.to_numeric(df['want'], errors='coerce')
                df['for_sale'] = pd.to_numeric(df['for_sale'], errors='coerce')
                filtered_df = filter_data(df,for_sale_threshold, have_threshold, want_threshold)
                
                if not filtered_df.empty:
                    st.subheader("Filtered Data")
                    if 'url' in filtered_df.columns:
                        st.data_editor(
                            filtered_df,
                            hide_index=True,
                        )
                    else:
                        st.dataframe(filtered_df)
                else:
                    st.write("No rows found based on the selected threshold.")
            else:
                st.write("Empty DataFrame retrieved from the database.")
        else:
            st.write("Failed to retrieve data from the database.")

