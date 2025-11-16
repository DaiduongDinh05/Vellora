import { View, Text, Pressable, SafeAreaView } from "react-native";
import { rateStyles } from "../styles/ReimbursementStyles";

type IRSPageProps = {
  onBack?: () => void;
};

const irsRates = [
  { label: "Business", value: "$0.70" },
  { label: "Charity", value: "$0.14" },
  { label: "Medical moving", value: "$0.21" },
  { label: "Military moving", value: "$0.21" },
  { label: "Personal", value: "$0.00" },
];

export default function ViewIRSRatePage({ onBack }: IRSPageProps) {
  return (
    <SafeAreaView style={rateStyles.safe}>
      <View style={rateStyles.screenContainer}>
        <View style={rateStyles.headerRow}>
          <Pressable
            onPress={onBack}
            style={rateStyles.headerBackHitbox}
          >
            <Text style={rateStyles.headerBackText}>{"<"}</Text>
          </Pressable>
          <Text style={rateStyles.headerTitle}>IRS Standard Mileage Rate</Text>
        </View>

        <Text style={rateStyles.paragraph}>
          Below is the IRS set standard mileage rate for US
        </Text>

        <View style={rateStyles.card}>
          <View style={rateStyles.cardSectionHeader}>
            <Text style={rateStyles.sectionLabel}>RATES</Text>
          </View>
          <View style={rateStyles.divider} />

          {irsRates.map((r, idx) => (
            <View key={r.label}>
              <View style={rateStyles.rateRow}>
                <Text style={rateStyles.rateRowText}>{r.label}</Text>
                <Text style={rateStyles.rateRowPrice}>{r.value}</Text>
              </View>
              {idx < irsRates.length - 1 && <View style={rateStyles.divider} />}
            </View>
          ))}
        </View>
      </View>
    </SafeAreaView>
  );
}
