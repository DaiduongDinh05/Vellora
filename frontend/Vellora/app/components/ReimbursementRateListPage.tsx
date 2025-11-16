import { View, Text, Pressable, SafeAreaView, FlatList } from "react-native";
import { rateStyles } from "../styles/ReimbursementStyles";
import type { CustomRate } from "../reimbursement";

type Props = {
	rates: CustomRate[];
	onCreateCustom: () => void;
	onOpenIRS: () => void;
	onOpenCustomRate: (id: string) => void;
	onDelete: (id: string) => void;
	deletingId: string | null;
};

export default function ReimbursementRateListPage({
	rates,
	onCreateCustom,
	onOpenIRS,
	onOpenCustomRate,
	onDelete,
	deletingId,
}: Props) {
	return (
		<SafeAreaView style={rateStyles.safe}>
			<View style={rateStyles.screenContainer}>
				<View style={rateStyles.headerRow}>
					<Text style={rateStyles.headerTitle}>Reimbursement rate</Text>
				</View>

				<Text style={rateStyles.paragraph}>
					Personalize your experience by selecting or adding a custom mileage
					reimbursement rate
				</Text>

				<View style={rateStyles.card}>
					<Pressable onPress={onOpenIRS}>
						<Text style={rateStyles.listItem}>IRS Standard Rates</Text>
					</Pressable>

					<FlatList
						data={rates}
						keyExtractor={(item) => item.id}
						renderItem={({ item }) => (
							<View style={{ flexDirection: "row", alignItems: "center" }}>
								<Pressable
									style={{ flex: 1 }}
									onPress={() => onOpenCustomRate(item.id)}>
									<Text style={rateStyles.listItem}>{item.name}</Text>
								</Pressable>
								<Pressable
									onPress={() => onDelete(item.id)}
									disabled={deletingId === item.id}
									style={{
										paddingHorizontal: 12,
										paddingVertical: 12,
										opacity: deletingId === item.id ? 0.5 : 1,
									}}>
									<Text style={{ color: "#EF4444", fontSize: 14 }}>Delete</Text>
								</Pressable>
							</View>
						)}
					/>

					<Pressable onPress={onCreateCustom}>
						<Text style={rateStyles.addCustom}>+ Create custom rate</Text>
					</Pressable>
				</View>
			</View>
		</SafeAreaView>
	);
}
