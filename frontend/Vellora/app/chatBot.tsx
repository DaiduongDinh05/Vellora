import { View, Text, Image, TextInput, Pressable, StyleSheet, StatusBar } from "react-native";
import { router } from "expo-router";
import { FontAwesome } from "@expo/vector-icons";

export default function chatBot() {
	return (
		<View style={styles.container}>
			<StatusBar barStyle="light-content" backgroundColor="#404CCF" />
			<View style={styles.header}>
				<Pressable onPress={() => router.back()} style={styles.backButton}>
					<FontAwesome name="chevron-left" size={20} color="#FFFFFF" />
				</Pressable>
				<Text style={styles.headerTitle}>Velo</Text>
				<View style={styles.headerSpacer} />
			</View>

			<View style={styles.content}>
				<Image source={require("./assets/wheel.png")} style={styles.wheelTop} />
				<Image source={require("./assets/wheel.png")} style={styles.wheelBottomLeft} />
				<Image source={require("./assets/wheel.png")} style={styles.wheelBottomRight} />

				<View style={styles.mascotContainer}>
					<Image 
						source={require("./assets/velo.png")} 
						style={styles.mascotImage} 
						resizeMode="contain"
					/>
				</View>
			</View>

			<View style={styles.inputContainer}>
				<View style={styles.inputWrapper}>
					<TextInput
						style={styles.textInput}
						placeholder="Ask your question..."
						placeholderTextColor="#999"
						multiline
					/>
					<Pressable style={styles.sendButton}>
						<View style={styles.sendIconContainer}>
							<View style={styles.linesContainer}>
								<View style={styles.line1} />
								<View style={styles.line2} />
								<View style={styles.line3} />
							</View>
							<Image source={require("./assets/wheel.png")} style={styles.wheelBackground} />
						</View>
					</Pressable>
				</View>
			</View>
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
		backgroundColor: "#131313",
	},
	header: {
		flexDirection: "row",
		alignItems: "center",
		paddingHorizontal: 20,
		paddingVertical: 15,
		paddingTop: 50,
		backgroundColor: "#404CCF",
	},
	backButton: {
		width: 40,
		height: 40,
		justifyContent: "center",
		alignItems: "flex-start",
	},
	headerTitle: {
		flex: 1,
		textAlign: "center",
		fontSize: 25 ,
		fontWeight: "600",
		color: "#FFFFFF",
	},
	headerSpacer: {
		width: 40,
	},
	content: {
		flex: 1,
		position: "relative",
		justifyContent: "center",
		alignItems: "center",
	},
	wheelTop: {
		position: "absolute",
		top: 130,
		right: 30,
		width: 90,
		height: 90,
	},
	wheelBottomLeft: {
		position: "absolute",
		bottom: 190,
		left: 40,
		width: 70,
		height: 70,
	},
	wheelBottomRight: {
		position: "absolute",
		bottom: 160,
		left: 110,
		width: 50,
		height: 50,
	},
	mascotContainer: {
		alignItems: "center",
		justifyContent: "center",
	},
	mascotImage: {
		width: 500,
		height: 500,
	},
	inputContainer: {
		paddingHorizontal: 23,
		paddingBottom: 25,
		paddingTop: 10,
		marginBottom: 10
	},
	inputWrapper: {
		flexDirection: "row",
		alignItems: "flex-end",
		backgroundColor: "#272727",
		borderRadius: 15,
		paddingHorizontal: 15,
		paddingVertical: 5,
	},
	textInput: {
		flex: 1,
		color: "#FFFFFF",
		fontSize: 16,
		maxHeight: 100,
		paddingVertical: 8,
	},
	sendButton: {
		width: 30,
		height: 25,
		borderRadius: 0,
		justifyContent: "center",
		alignItems: "center",
		padding: 5,
		marginBottom: 6,
		right: 5
	},
	sendIconContainer: {
		width: 40,
		height: 25,
		justifyContent: "center",
		alignItems: "center",
		flexDirection: "row",
	},
	wheelBackground: {
		width: 20,
		height: 20,
	},
	linesContainer: {
		justifyContent: "space-around",
		alignItems: "flex-end",
		marginRight: 3,
		height: 12,
		flexDirection: "column",
	},
	line1: {
		width: 15,
		height: 1,
		backgroundColor: "#4DBF69",
		marginBottom: 2,
	},
	line2: {
		width: 10,
		height: 1,
		backgroundColor: "#4DBF69",
		marginBottom: 2,
	},
	line3: {
		width: 5,
		height: 1,
		backgroundColor: "#4DBF69",
	},
});