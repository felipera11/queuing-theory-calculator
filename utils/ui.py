import streamlit as st


def format_display_value(value):
	if isinstance(value, int):
		return str(value)

	if isinstance(value, float):
		if value.is_integer():
			return str(int(value))
		return f"{value:.4f}".rstrip("0").rstrip(".")

	text = str(value)
	try:
		numeric_value = float(text)
	except (TypeError, ValueError):
		return text

	if numeric_value.is_integer():
		return str(int(numeric_value))

	return f"{numeric_value:.4f}".rstrip("0").rstrip(".")


def inject_theme():
	st.markdown(
		"""
		<style>
		:root {
			--app-bg: #07111f;
			--panel-bg: #101a33;
			--panel-bg-2: #162242;
			--border-color: #263154;
			--primary-blue: #0f4c81;
			--primary-purple: #6d28d9;
			--primary-purple-2: #8b5cf6;
			--text-main: #f4f7ff;
			--text-muted: #b7c2e0;
		}

		.stApp {
			background: var(--app-bg);
			color: var(--text-main);
		}

		header,
		[data-testid="stHeader"],
		[data-testid="stToolbar"],
		[data-testid="stDecoration"],
		[data-testid="stMainMenu"],
		[data-testid="stDeployButton"],
		[data-testid="collapsedControl"],
		button[kind="header"],
		footer {
			background: transparent;
		}

		header,
		[data-testid="stMainMenu"],
		[data-testid="stDeployButton"],
		[data-testid="collapsedControl"],
		button[kind="header"],
		footer {
			display: none;
		}

		h1, h2, h3, h4, h5, h6, p, label, span, div {
			color: var(--text-main);
		}

		p, small, .stCaption, .stMarkdown, .stText {
			color: var(--text-muted);
		}

		[data-testid="stSidebar"] {
			background: #09101c;
			border-right: 1px solid var(--border-color);
		}

		.stButton > button {
			background: var(--primary-purple);
			color: white;
			border: 1px solid #9a7cf0;
			border-radius: 12px;
			padding: 0.55rem 1rem;
			font-weight: 600;
			transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
		}

		.stButton > button:hover {
			background: var(--primary-blue);
			border-color: #4aa3ff;
			transform: translateY(-1px);
		}

		.stButton > button:focus-visible {
			box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.35);
		}

		.stTextInput input,
		.stNumberInput input,
		.stTextArea textarea,
		.stSelectbox div[data-baseweb="select"] > div {
			background: var(--panel-bg);
			color: var(--text-main);
			border: 1px solid var(--border-color);
			border-radius: 10px;
		}

		.stTextInput input:focus,
		.stNumberInput input:focus,
		.stTextArea textarea:focus {
			border-color: var(--primary-purple-2);
			box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.25);
		}

		[data-baseweb="tab-list"] {
			gap: 0.4rem;
			border-bottom: 1px solid var(--border-color);
		}

		[data-baseweb="tab"] {
			background: var(--panel-bg);
			color: var(--text-muted);
			border: 1px solid var(--border-color);
			border-radius: 999px 999px 0 0;
			padding: 0.65rem 1rem;
			font-weight: 600;
		}

		[data-baseweb="tab"]:hover {
			color: var(--text-main);
			background: var(--panel-bg-2);
		}

		[data-baseweb="tab"][aria-selected="true"] {
			background: var(--primary-purple);
			color: white;
			border-color: var(--primary-purple-2);
		}

		.stMetric {
			background: linear-gradient(180deg, var(--panel-bg-2), var(--panel-bg));
			border: 1px solid var(--border-color);
			border-radius: 14px;
			padding: 1rem;
		}

		[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
			color: var(--text-main);
		}

		[data-testid="stAlert"] {
			border-radius: 12px;
		}
		</style>
		""",
		unsafe_allow_html=True,
	)


def metric_grid(items, columns=4):
	for index in range(0, len(items), columns):
		row = items[index : index + columns]
		cols = st.columns(len(row))
		for col, item in zip(cols, row):
			with col:
				with st.container(border=True):
					st.metric(item[0], format_display_value(item[1]))
