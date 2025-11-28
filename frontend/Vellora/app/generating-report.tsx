import { useState, useEffect } from "react";
import { View, Text, ActivityIndicator } from "react-native";
import { useLocalSearchParams, router } from "expo-router";
import ScreenLayout from "./components/ScreenLayout";
import { Colors } from "./Colors";

type ProgressState = "pending" | "processing" | "completed";

export default function GeneratingReportPage() {
	const params = useLocalSearchParams();
	const [progress, setProgress] = useState<ProgressState>("pending");
	const [progressPercent, setProgressPercent] = useState(0);

	useEffect(() => {
		const progressInterval = setInterval(() => {
			setProgressPercent((prev) => {
				if (prev < 33) {
					setProgress("pending");
					return Math.min(prev + 2, 33);
				} else if (prev < 66) {
					setProgress("processing");
					return Math.min(prev + 2, 66);
				} else {
					setProgress("completed");
					const newPercent = Math.min(prev + 2, 100);
					if (newPercent >= 100) {
						setTimeout(() => {
							router.replace({
								pathname: "/report-details",
								params: {
									fromDate: (params.fromDate as string) || "",
									toDate: (params.toDate as string) || "",
									status: "Completed",
									createdOn: new Date().toISOString(),
								},
							} as any);
						}, 500);
					}
					return newPercent;
				}
			});
		}, 100);

		return () => clearInterval(progressInterval);
	}, [params]);

	const getStatusText = () => {
		switch (progress) {
			case "pending":
				return "Pending";
			case "processing":
				return "Processing";
			case "completed":
				return "Completed";
		}
	};

	const getStatusColor = () => {
		switch (progress) {
			case "pending":
				return "#F59E0B";
			case "processing":
				return "#3B82F6";
			case "completed":
				return Colors.accentGreen;
		}
	};

	return (
		<ScreenLayout footer={<View />}>
			<View className="flex-1 px-6 pt-6 justify-center items-center">
				<Text className="text-3xl font-bold text-textBlack mb-8">
					Generating
				</Text>

				<ActivityIndicator
					size="large"
					color={Colors.primaryPurple}
					className="mb-8"
				/>

				<View className="w-full mb-4">
					<View className="w-full h-3 bg-backgroundGrey rounded-full overflow-hidden">
						<View
							className="h-full rounded-full transition-all duration-300"
							style={{
								width: `${progressPercent}%`,
								backgroundColor: getStatusColor(),
							}}
						/>
					</View>
				</View>

				<View className="flex-row justify-between w-full mb-2">
					<Text
						className={`text-sm font-semibold ${
							progress === "pending" ? "text-primaryPurple" : "text-gray-400"
						}`}>
						Pending
					</Text>
					<Text
						className={`text-sm font-semibold ${
							progress === "processing" ? "text-primaryPurple" : "text-gray-400"
						}`}>
						Processing
					</Text>
					<Text
						className={`text-sm font-semibold ${
							progress === "completed" ? "text-accentGreen" : "text-gray-400"
						}`}>
						Completed
					</Text>
				</View>

				<Text className="text-base text-gray-600 mt-4">
					{getStatusText()}...
				</Text>
			</View>
		</ScreenLayout>
	);
}
