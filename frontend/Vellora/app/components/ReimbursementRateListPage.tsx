import { useState } from "react"
import { View, Text, Pressable, SafeAreaView } from "react-native"
import { rateStyles } from "../styles/ReimbursementStyles"
import AddCustomRatePage from "./AddCustomRatePage"

export default function ReimbursementRateListPage() {
  const [showAdd, setShowAdd] = useState(false)
  const [customRates, setCustomRates] = useState<any[]>([])

  return (
    <SafeAreaView style={rateStyles.safe}>
      <View style={rateStyles.screenContainer}>
        <View style={rateStyles.headerRow}>
          <Text style={rateStyles.headerTitle}>Reimbursement rate</Text>
        </View>

        <Text style={rateStyles.paragraph}>
          Personalize your experience by selecting or adding a custom mileage reimbursement rate
        </Text>

        <View style={rateStyles.card}>
          <View style={rateStyles.cardSectionHeader}>
            <Text style={rateStyles.sectionLabel}>RATES</Text>
          </View>

          <View style={rateStyles.divider} />

          <Pressable
            onPress={() => setShowAdd(true)}
            style={rateStyles.addRow}
          >
            <View style={rateStyles.addIconCircle}>
              <Text style={rateStyles.addIconText}>+</Text>
            </View>
            <Text style={rateStyles.addText}>Create a custom reimbursement rate</Text>
          </Pressable>

          <View style={rateStyles.divider} />

          <Pressable style={rateStyles.rateRow}>
            <Text style={rateStyles.rateRowText}>IRS Standard Mileage Rate</Text>
            <Text style={rateStyles.rowChevron}>{">"}</Text>
          </Pressable>

          {customRates.length > 0 && <View style={rateStyles.divider} />}

          {customRates.map((r) => (
            <View key={r.id}>
              <Pressable style={rateStyles.rateRow}>
                <Text style={rateStyles.rateRowText}>
                  {r.name} ({r.year})
                </Text>
                <Text style={rateStyles.rowChevron}>{">"}</Text>
              </Pressable>
              <View style={rateStyles.divider} />
            </View>
          ))}
        </View>
      </View>

      {showAdd && (
        <View
          style={{
            position: "absolute",
            inset: 0,
            zIndex: 999,
            backgroundColor: "white",
            elevation: 20
          }}
          pointerEvents="auto"
        >
          <AddCustomRatePage
            onClose={() => setShowAdd(false)}
            onSave={(data) => {
              const newRate = {
                id: `${Date.now()}`,
                name: data.name,
                description: data.description,
                year: data.year,
                categories: data.categories
              }
              setCustomRates((prev) => [...prev, newRate])
              setShowAdd(false)
            }}
          />
        </View>
      )}
    </SafeAreaView>
  )
}
