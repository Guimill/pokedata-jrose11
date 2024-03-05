# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import streamlit as st
from streamlit.logger import get_logger
import base64
from pathlib import Path

LOGGER = get_logger(__name__)


st.set_page_config(
        page_title="Pokedata Jroose",
        page_icon="🎮")

with open("/workspaces/pokedata-jroose11/static/Sprite_0065_RB.png", "rb") as f:
    data = base64.b64encode(f.read()).decode("utf-8")

st.markdown(
        f"""
                <div>
                        <h1>Welcome to Pokedata Jroose 11 !
                        <img src="data:image/png;base64,{data}" width="60" height="60" style="padding-bottom: 10px">
                </div>
        """, unsafe_allow_html=True)


st.markdown(
        """

        This webapp is design to give interpretetions and interactivness on the binding beetween [Jroose11](https://www.youtube.com/@Jrose11) runs and the datas from pokemon gen 1

        I hope you'll find it usefull and fun !

        I want to thank [Jroose11](https://www.youtube.com/@Jrose11) for it's work and all people that work or have been working on sites that provides pokedatas, especially Bulbapedia, Pokepédia and Westwood : https://github.com/EverOddish/Westwood.
        And also, all people that work for the libraries that I used.

        Enjoy !

        """)

st.success("By Milleret Guillaume : [Github](https://github.com/Guimill), [Linkedin](https://www.linkedin.com/in/guillaume-milleret/), Mail: guillaume.milleret@gmail.com")

