import { StyleSheet } from "react-native";

const BLUE = "#3F46D6";

export const styles = StyleSheet.create({
	safe: {
		flex: 1,
		backgroundColor: "#fff",
	},
	container: {
		flex: 1,
		paddingHorizontal: 24,
		paddingTop: 64,
	},
	logoRow: {
		flexDirection: "row",
		alignItems: "center",
		marginBottom: 40,
	},
	logoText: {
		fontSize: 48,
		fontWeight: "800",
		color: BLUE,
		letterSpacing: 0.5,
	},
	logoMark: {
		width: 28,
		height: 28,
		marginHorizontal: 4,
		borderRadius: 14,
		backgroundColor: "#22C55E",
		alignItems: "center",
		justifyContent: "center",
	},
	logoMarkInner: {
		width: 14,
		height: 14,
		borderRadius: 7,
		backgroundColor: "#fff",
	},
	fieldGroup: {
		marginTop: 18,
	},
	label: {
		color: BLUE,
		fontSize: 14,
		marginBottom: 10,
	},
	input: {
		height: 40,
		borderBottomWidth: 1,
		borderBottomColor: "#111",
		fontSize: 16,
		paddingVertical: 4,
	},
	cta: {
		marginTop: 36,
		backgroundColor: BLUE,
		height: 52,
		borderRadius: 12,
		alignItems: "center",
		justifyContent: "center",
	},
	ctaText: {
		color: "#fff",
		fontSize: 18,
		fontWeight: "700",
	},
	footerText: {
		marginTop: 14,
		textAlign: "center",
		color: "#111",
	},
	link: {
		color: BLUE,
		fontWeight: "700",
	},
});
