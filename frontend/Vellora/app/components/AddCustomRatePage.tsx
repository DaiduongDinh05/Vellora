import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { rateStyles } from "../styles/ReimbursementStyles";

type AddCustomRateProps = {
  onClose?: () => void;
  onSave?: () => void;
};

type Category = {
  id: string;
  name: string;
  rate: number;
};

export default function AddCustomRatePage({
  onClose,
  onSave,
}: AddCustomRateProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [year, setYear] = useState("");
  const [categories, setCategories] = useState<Category[]>([
    { id: "business", name: "Business", rate: 0.4 },
    { id: "personal", name: "Personal", rate: 0.1 },
  ]);
  const [isAddingCategory, setIsAddingCategory] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");

  const handleAddCategoryRow = () => {
    setIsAddingCategory(true);
    setNewCategoryName("");
  };

  const commitNewCategory = () => {
    const trimmed = newCategoryName.trim();
    if (!trimmed) {
      setIsAddingCategory(false);
      setNewCategoryName("");
      return;
    }
    const next: Category = {
      id: `${Date.now()}`,
      name: trimmed,
      rate: 0,
    };
    setCategories([next, ...categories]);
    setIsAddingCategory(false);
    setNewCategoryName("");
  };

  const handleSave = () => {
    if (onSave) onSave();
  };

  return (
    <SafeAreaView style={rateStyles.safe}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        <View style={rateStyles.fullScreenWhite}>
          <View style={rateStyles.formHeaderRow}>
            <Pressable
              onPress={onClose}
              style={rateStyles.closeCircle}
            >
              <Text style={rateStyles.closeText}>×</Text>
            </Pressable>
            <Text style={rateStyles.formTitle}>Add custom rate</Text>
          </View>

          <View style={rateStyles.formFieldGroup}>
            <Text style={rateStyles.formLabel}>Name</Text>
            <TextInput
              style={rateStyles.formInput}
              placeholder="Enter a name for custom rate"
              placeholderTextColor="#9CA3AF"
              value={name}
              onChangeText={setName}
            />
          </View>

          <View style={rateStyles.formFieldGroup}>
            <Text style={rateStyles.formLabel}>Description</Text>
            <TextInput
              style={rateStyles.formInput}
              placeholder="Enter a description for custom rate"
              placeholderTextColor="#9CA3AF"
              value={description}
              onChangeText={setDescription}
            />
          </View>

          <View style={rateStyles.formFieldGroup}>
            <Text style={rateStyles.formLabel}>Year</Text>
            <TextInput
              style={[rateStyles.formInput, { width: 120 }]}
              placeholder="YYYY"
              placeholderTextColor="#9CA3AF"
              keyboardType="numeric"
              maxLength={4}
              value={year}
              onChangeText={setYear}
            />
          </View>

          <View style={rateStyles.formHeadingRow}>
            <Text style={rateStyles.sectionLabel}>Categories and costs</Text>
          </View>

          <View style={{ marginTop: 8 }}>
            {!isAddingCategory && (
              <Pressable
                onPress={handleAddCategoryRow}
                style={rateStyles.addRow}
              >
                <View style={rateStyles.addIconCircle}>
                  <Text style={rateStyles.addIconText}>+</Text>
                </View>
                <Text style={rateStyles.addText}>Add a category</Text>
              </Pressable>
            )}

            {isAddingCategory && (
              <View>
                <View style={rateStyles.divider} />
                <View style={rateStyles.rateRow}>
                  <View style={rateStyles.minusIcon} />
                  <TextInput
                    style={rateStyles.categoryInput}
                    placeholder="Enter new category for reimbursement"
                    placeholderTextColor="#9CA3AF"
                    value={newCategoryName}
                    onChangeText={setNewCategoryName}
                    onBlur={commitNewCategory}
                    onSubmitEditing={commitNewCategory}
                    returnKeyType="done"
                  />
                  <Text style={[rateStyles.rateRowPrice, { color: "#9CA3AF" }]}>
                    $0.00
                  </Text>
                </View>
              </View>
            )}

            <View style={rateStyles.divider} />

            {categories.map((c, idx) => (
              <View key={c.id}>
                <View style={rateStyles.rateRow}>
                  <View style={rateStyles.minusIcon} />
                  <Text style={rateStyles.rateRowText}>{c.name}</Text>
                  <Text style={rateStyles.rateRowPrice}>
                    ${c.rate.toFixed(2)}
                  </Text>
                </View>
                {idx < categories.length - 1 && (
                  <View style={rateStyles.divider} />
                )}
              </View>
            ))}
          </View>

          <Pressable
            onPress={handleSave}
            style={rateStyles.formSaveButton}
          >
            <Text style={rateStyles.formSaveText}>Save</Text>
          </Pressable>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}
