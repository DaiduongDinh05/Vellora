import { useState } from "react";
import { View, Text, Pressable } from "react-native";
import { router } from "expo-router";
import DateTimePicker, {
	DateTimePickerEvent,
} from "@react-native-community/datetimepicker";
import ScreenLayout from "../components/ScreenLayout";
import Button from "../components/Button";
import { reportStyles } from "../styles/ReportStyles";

export default function GenerateReportPage() {
	const [fromDate, setFromDate] = useState<Date>(new Date());
	const [toDate, setToDate] = useState<Date>(new Date());
	const [showFromPicker, setShowFromPicker] = useState(false);
	const [showToPicker, setShowToPicker] = useState(false);

	const handleFromDateChange = (
		event: DateTimePickerEvent,
		selectedDate?: Date
	) => {
		setShowFromPicker(false);
		if (selectedDate) {
			setFromDate(selectedDate);
		}
	};

	const handleToDateChange = (
		event: DateTimePickerEvent,
		selectedDate?: Date
	) => {
		setShowToPicker(false);
		if (selectedDate) {
			setToDate(selectedDate);
		}
	};

	const formatDate = (date: Date): string => {
		return date.toLocaleDateString("en-US", {
			year: "numeric",
			month: "short",
			day: "numeric",
		});
	};

	return (
		<ScreenLayout
			footer={
				<View>
					<Pressable
						style={reportStyles.historyButton}
						onPress={() => router.push("/report-details" as any)}>
						<Text style={reportStyles.historyText}>View Report History</Text>
					</Pressable>
					<Button
						title="Generate Report"
						onPress={() =>
							router.push({
								pathname: "/generating-report",
								params: {
									fromDate: fromDate.toISOString(),
									toDate: toDate.toISOString(),
								},
							} as any)
						}
						className="mt-3"
					/>
				</View>
			}>
			<View className="flex-1 px-6 pt-6">
				<Text style={reportStyles.title}>Generate Report</Text>

				<Text style={reportStyles.sectionLabel}>Select Date Range</Text>

				<View style={reportStyles.card}>
					<Text style={reportStyles.inputLabel}>From Date</Text>
					<Pressable
						style={reportStyles.inputBox}
						onPress={() => setShowFromPicker(true)}>
						<Text style={reportStyles.inputText}>{formatDate(fromDate)}</Text>
					</Pressable>
					{showFromPicker && (
						<DateTimePicker
							value={fromDate}
							mode="date"
							display="default"
							onChange={handleFromDateChange}
						/>
					)}

					<Text style={[reportStyles.inputLabel, { marginTop: 16 }]}>
						To Date
					</Text>
					<Pressable
						style={reportStyles.inputBox}
						onPress={() => setShowToPicker(true)}>
						<Text style={reportStyles.inputText}>{formatDate(toDate)}</Text>
					</Pressable>
					{showToPicker && (
						<DateTimePicker
							value={toDate}
							mode="date"
							display="default"
							onChange={handleToDateChange}
						/>
					)}
				</View>
			</View>
		</ScreenLayout>
	);
}
