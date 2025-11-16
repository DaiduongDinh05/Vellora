import { View, Text, Pressable, SafeAreaView } from "react-native";
import { rateStyles } from "../styles/ReimbursementStyles";

type CustomRatePageProps = {
  onBack?: () => void;
};

const sampleCustomRate = {
  name: "Custom rate 1",
  description: "This is just a test custom rate",
  categories: [
    { label: "Business", value: "$0.50" },
    { label: "Charity", value: "$0.20" },
    { label: "Personal", value: "$0.05" },
  ],
};

export default function ViewCustomRatePage({ onBack }: CustomRatePageProps) {
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
          <Text style={rateStyles.headerTitle}>{sampleCustomRate.name}</Text>
        </View>

        <Text style={rateStyles.paragraph}>{sampleCustomRate.description}</Text>

        <View style={rateStyles.card}>
          <View style={rateStyles.cardSectionHeader}>
            <Text style={rateStyles.sectionLabel}>RATES</Text>
          </View>
          <View style={rateStyles.divider} />

          {sampleCustomRate.categories.map((r, idx) => (
            <View key={r.label}>
              <View style={rateStyles.rateRow}>
                <Text style={rateStyles.rateRowText}>{r.label}</Text>
                <Text style={rateStyles.rateRowPrice}>{r.value}</Text>
              </View>
              {idx < sampleCustomRate.categories.length - 1 && (
                <View style={rateStyles.divider} />
              )}
            </View>
          ))}
        </View>
      </View>
    </SafeAreaView>
  );
}
