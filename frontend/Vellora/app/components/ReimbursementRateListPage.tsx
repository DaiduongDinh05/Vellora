import { View, Text, Pressable, SafeAreaView } from "react-native";
import { rateStyles } from "../styles/ReimbursementStyles";

type RateListProps = {
  onCreateCustom?: () => void;
  onOpenIRS?: () => void;
  onOpenCustomRate?: (id: string) => void;
};

export default function ReimbursementRateListPage({
  onCreateCustom,
  onOpenIRS,
  onOpenCustomRate,
}: RateListProps) {
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
          <View style={rateStyles.cardSectionHeader}>
            <Text style={rateStyles.sectionLabel}>RATES</Text>
          </View>

          <View style={rateStyles.divider} />

          <Pressable onPress={onCreateCustom} style={rateStyles.addRow}>
            <View style={rateStyles.addIconCircle}>
              <Text style={rateStyles.addIconText}>+</Text>
            </View>
            <Text style={rateStyles.addText}>
              Create a custom reimbursement rate
            </Text>
          </Pressable>

          <View style={rateStyles.divider} />

          <Pressable onPress={onOpenIRS} style={rateStyles.rateRow}>
            <Text style={rateStyles.rateRowText}>
              IRS Standard Mileage Rate
            </Text>
            <Text style={rateStyles.rowChevron}>{">"}</Text>
          </Pressable>

          <View style={rateStyles.divider} />

          <Pressable
            onPress={() => onOpenCustomRate?.("custom-1")}
            style={rateStyles.rateRow}
          >
            <Text style={rateStyles.rateRowText}>Custom rate 1</Text>
            <Text style={rateStyles.rowChevron}>{">"}</Text>
          </Pressable>
        </View>
      </View>
    </SafeAreaView>
  );
}
