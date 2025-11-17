import { useEffect, useState } from "react";
import { View, Text, ActivityIndicator } from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import { tokenStorage } from "../../services/tokenStorage";

export default function OAuthCallback() {
	const params = useLocalSearchParams();
	const [error, setError] = useState<string | null>(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const processCallback = async () => {
			try {
				const accessToken = params.access_token as string;

				if (!accessToken) {
					setError("Missing access token.");
					setLoading(false);
					return;
				}

				tokenStorage.setToken(accessToken);

				const redirect = params.redirect as string;
				if (redirect) {
					router.replace(redirect as any);
				} else {
					router.replace("/(tabs)");
				}
			} catch (err) {
				setError(err instanceof Error ? err.message : "Authentication failed.");
				setLoading(false);
			}
		};

		processCallback();
	}, [params]);

	if (loading) {
		return (
			<View
				style={{
					flex: 1,
					justifyContent: "center",
					alignItems: "center",
					backgroundColor: "#fff",
				}}>
				<ActivityIndicator size="large" color="#000" />
				<Text style={{ marginTop: 16, fontSize: 16 }}>
					Completing sign in...
				</Text>
			</View>
		);
	}

	if (error) {
		return (
			<View
				style={{
					flex: 1,
					justifyContent: "center",
					alignItems: "center",
					backgroundColor: "#fff",
					padding: 20,
				}}>
				<Text style={{ fontSize: 16, color: "#ef4444", textAlign: "center" }}>
					{error}
				</Text>
				<Text
					style={{
						marginTop: 20,
						fontSize: 14,
						color: "#3b82f6",
						textDecorationLine: "underline",
					}}
					onPress={() => router.replace("/login")}>
					Return to Login
				</Text>
			</View>
		);
	}

	return null;
}
