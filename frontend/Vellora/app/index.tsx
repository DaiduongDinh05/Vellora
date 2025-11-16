import { View, Text, Pressable, SafeAreaView } from "react-native";
import { router } from "expo-router";

export default function Index() {
	return (
		<SafeAreaView
			style={{
				flex: 1,
				backgroundColor: "#fff",
				justifyContent: "center",
				alignItems: "center",
				padding: 20,
			}}>
			<Pressable
				onPress={() => router.push("/login" as any)}
				style={{
					width: "100%",
					paddingVertical: 16,
					backgroundColor: "#3F46D6",
					borderRadius: 12,
				}}>
				<Text
					style={{
						color: "#fff",
						textAlign: "center",
						fontSize: 18,
						fontWeight: "600",
					}}>
					Login
				</Text>
			</Pressable>
		</SafeAreaView>
	);
}
