import {
	View,
	Text,
	ScrollView,
	TouchableOpacity,
	Pressable,
} from "react-native";
import ScreenLayout from "./components/ScreenLayout";
import { Colors } from "./Colors";

type Report = {
	id: string;
	range: string;
	status: "Completed" | "Failed";
	created: string;
	action: "Download" | "Regenerate" | "Retry";
};

export default function ReportDetailsPage() {
	// API call here
	const reports: Report[] = [
		{
			id: "1",
			range: "Jan 1 - Jan 31",
			status: "Completed",
			created: "Feb 2",
			action: "Download",
		},
		{
			id: "2",
			range: "Jan 1 - Jan 31",
			status: "Completed",
			created: "Feb 2",
			action: "Regenerate",
		},
		{
			id: "3",
			range: "Jan 1 - Jan 31",
			status: "Completed",
			created: "Feb 2",
			action: "Retry",
		},
		{
			id: "4",
			range: "Jan 1 - Jan 31",
			status: "Completed",
			created: "Feb 2",
			action: "Regenerate",
		},
		{
			id: "5",
			range: "Jan 1 - Jan 31",
			status: "Completed",
			created: "Feb 2",
			action: "Regenerate",
		},
	];

	const handleAction = (report: Report) => {
		// backend for the download/regenerate/retry actions
	};

	const handleRefresh = () => {
		//  Refresh reports list from API
	};

	return (
		<ScreenLayout footer={<View />}>
			<View className="flex-1 bg-backgroundGrey">
				<View className="bg-white px-6 pt-12 pb-4 flex-row items-center justify-between border-b border-gray-200">
					<View className="flex-1" />
					<Text
						className="text-xl font-bold flex-1 text-center"
						style={{ color: Colors.primaryPurple }}>
						Reports History
					</Text>
					<View className="flex-1 items-end">
						<Pressable
							onPress={handleRefresh}
							className="bg-accentGreen px-4 py-2 rounded-lg">
							<Text className="text-white font-semibold text-sm">Refresh</Text>
						</Pressable>
					</View>
				</View>

				<View className="bg-white px-6 py-3 flex-row border-b border-gray-200">
					<View className="flex-1">
						<Text
							className="text-sm font-semibold"
							style={{ color: Colors.primaryPurple }}>
							Range
						</Text>
					</View>
					<View className="flex-1">
						<Text
							className="text-sm font-semibold"
							style={{ color: Colors.primaryPurple }}>
							Status
						</Text>
					</View>
					<View className="flex-1">
						<Text
							className="text-sm font-semibold"
							style={{ color: Colors.primaryPurple }}>
							Created
						</Text>
					</View>
					<View className="flex-1">
						<Text
							className="text-sm font-semibold"
							style={{ color: Colors.primaryPurple }}>
							Action
						</Text>
					</View>
				</View>

				<ScrollView className="flex-1">
					{reports.map((report) => (
						<View
							key={report.id}
							className="bg-white px-6 py-4 flex-row items-center border-b border-gray-200">
							<View className="flex-1">
								<Text className="text-sm text-textBlack">{report.range}</Text>
							</View>
							<View className="flex-1">
								<Text
									className="text-sm font-medium"
									style={{
										color:
											report.status === "Completed"
												? Colors.accentGreen
												: "#EF4444",
									}}>
									{report.status}
								</Text>
							</View>
							<View className="flex-1">
								<Text className="text-sm text-textBlack">{report.created}</Text>
							</View>
							<View className="flex-1">
								<TouchableOpacity onPress={() => handleAction(report)}>
									<Text
										className="text-sm underline"
										style={{ color: Colors.primaryPurple }}>
										{report.action}
									</Text>
								</TouchableOpacity>
							</View>
						</View>
					))}
				</ScrollView>
			</View>
		</ScreenLayout>
	);
}
