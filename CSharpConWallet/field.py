"""This module returns the passphrase, &
    PureStake Mainnet & Testnet Client Instance"""

from algosdk.v2client import algod
from CSharpConWallet.models import admin_data


def get_passphrase():
    """_summary_
    This function is used to store the passphrase
    """

    holders = {
        "Words1": {
            "word1": "1",
            "word2": "2",
            "word3": "3",
            "word4": "4",
            "word5": "5",
        },
        "Words2": {
            "word6": "6",
            "word7": "7",
            "word8": "8",
            "word9": "9",
            "word10": "10",
        },
        "Words3": {
            "word11": "11",
            "word12": "12",
            "word13": "13",
            "word14": "14",
            "word15": "15",
        },
        "Words4": {
            "word16": "16",
            "word17": "17",
            "word18": "18",
            "word19": "19",
            "word20": "20",
        },
        "Words5": {
            "word21": "21",
            "word22": "22",
            "word23": "23",
            "word24": "24",
            "word25": "25",
        },
    }
    return holders


class PurestakeTestnet:
    """_summary_
    This class returns an instance of the PureStake Testnet Client
    """

    #dbdata = admin_data.objects.filter(key="PureStake").values("values")
    algod_token = "VfIjO0OLbD5COhQ2mgJIx40rJ1vXwpb4apvfdLpm"
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    purestake_token = {"X-Api-key": algod_token}
    algodclient = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)


class PurestakeMainnet:
    """_summary_
    This class returns an instance of the PureStake Mainnet Client
    """

    #dbdata = admin_data.objects.filter(key="PureStake").values("values")
    algod_token = "VfIjO0OLbD5COhQ2mgJIx40rJ1vXwpb4apvfdLpm"
    algod_address = "https://mainnet-algorand.api.purestake.io/ps2"
    purestake_token = {"X-Api-key": algod_token}
    algodclient = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)


class VerifyWords:
    """_summary_
    This class is used to store the passphrase
    for verification of passphrase
    """

    def __init__(
        self,
        word1,
        word2,
        word3,
        word4,
        word5,
        word6,
        word7,
        word8,
        word9,
        word10,
        word11,
        word12,
        word13,
        word14,
        word15,
    ):
        """_summary_

        Args:
            word1
            word2
            word3
            word4
            word5
            word6
            word7
            word8
            word9
            word10
            word11
            word12
            word13
            word14
            word15
        """
        self.data1 = word1
        self.data2 = word2
        self.data3 = word3
        self.data4 = word4
        self.data5 = word5
        self.data6 = word6
        self.data7 = word7
        self.data8 = word8
        self.data9 = word9
        self.data10 = word10
        self.data11 = word11
        self.data12 = word12
        self.data13 = word13
        self.data14 = word14
        self.data15 = word15

    def verify_feilds(self):
        """_summary_

        Returns: Dictory of all the passphrase words
        """
        holders = {
            "Words1": {
                "word1": self.data1,
                "word2": self.data2,
                "word3": self.data3,
                "word4": self.data4,
                "word5": self.data5,
            },
            "Words2": {
                "word6": self.data6,
                "word7": self.data7,
                "word8": self.data8,
                "word9": self.data9,
                "word10": self.data10,
            },
            "Words3": {
                "word11": self.data11,
                "word12": self.data12,
                "word13": self.data13,
                "word14": self.data14,
                "word15": self.data15,
            },
        }
        return holders


class GetpassField:
    """_summary_"""

    def __init__(
        self,
        word1,
        word2,
        word3,
        word4,
        word5,
        word6,
        word7,
        word8,
        word9,
        word10,
        word11,
        word12,
        word13,
        word14,
        word15,
        word16,
        word17,
        word18,
        word19,
        word20,
        word21,
        word22,
        word23,
        word24,
        word25,
    ):
        """_summary_

        Args:
            word1
            word2
            word3
            word4
            word5
            word6
            word7
            word8
            word9
            word10
            word11
            word12
            word13
            word14
            word15
        """
        self.data1 = word1
        self.data2 = word2
        self.data3 = word3
        self.data4 = word4
        self.data5 = word5
        self.data6 = word6
        self.data7 = word7
        self.data8 = word8
        self.data9 = word9
        self.data10 = word10
        self.data11 = word11
        self.data12 = word12
        self.data13 = word13
        self.data14 = word14
        self.data15 = word15
        self.data16 = word16
        self.data17 = word17
        self.data18 = word18
        self.data19 = word19
        self.data20 = word20
        self.data21 = word21
        self.data22 = word22
        self.data23 = word23
        self.data24 = word24
        self.data25 = word25

    def getpass_words(self):
        """_summary_
        Returns: Dictory of all the passphrase words
        """
        holders = {
            "Words1": {
                "word1": self.data1,
                "word2": self.data2,
                "word3": self.data3,
                "word4": self.data4,
                "word5": self.data5,
            },
            "Words2": {
                "word6": self.data6,
                "word7": self.data7,
                "word8": self.data8,
                "word9": self.data9,
                "word10": self.data10,
            },
            "Words3": {
                "word11": self.data11,
                "word12": self.data12,
                "word13": self.data13,
                "word14": self.data14,
                "word15": self.data15,
            },
            "Words4": {
                "word16": self.data16,
                "word17": self.data17,
                "word18": self.data18,
                "word19": self.data19,
                "word20": self.data20,
            },
            "Words5": {
                "word21": self.data21,
                "word22": self.data22,
                "word23": self.data23,
                "word24": self.data24,
                "word25": self.data25,
            },
        }
        return holders


class NetAPI:
    """_summary_
    This class return an instance of Network
    """

    def __init__(self, network):
        """_summary_

        Args: network
        """
        self.network = network

    def data_data(self):
        """_summary_

        Returns: Object: AlgoClient
        """
        net = self.network
        #dbdata = admin_data.objects.filter(key="PureStake").values("values")
        algod_token = "VfIjO0OLbD5COhQ2mgJIx40rJ1vXwpb4apvfdLpm"
        algod_address = "https://" + net + "-algorand.api.purestake.io/ps2"
        purestake_token = {"X-Api-key": algod_token}
        algodclient = algod.AlgodClient(
            algod_token, algod_address, headers=purestake_token
        )
        return algodclient


def UserReport():
    Report = {
        "personal": {
            "Name": "Michael Dershem",
            "Patient_Identifiers": [
                "81545862900a81d65c1f3c94 OID: 1.3.6.1.4.1.52618.1.1",
                "DOCS1393815124518198513 OID: 1.3.6.1.4.1.52618.1.1",
            ],
            "Date_of_Birth": "07/5/1963",
            "Sex": "Male",
            "CONTACT": "22 Oak Ridge Drive 22 Oak Ridge Dr Voorhees, NJ 8043, US",
        },
        "INSURANCE_PROVIDERS": [
            {
                "Plan": "TRAVELER AUTO INSURANCE",
                "Claim_Address": "P.O. BOX 430, BUFFALO, NY 14240",
                "Claims_Phone": "+1-800-842-2475",
                "Policy_Number": "80001301",
                "Group_Number": "80001301",
                "Relation": "Self",
                "Employer": "N/A",
                "Guarantor_Name": "Michael Dershem",
                "Guarantor_DoB": "07/5/1963",
                "Guarantor_Address": "22 Oak Ridge Drive 22 Oak Ridge Dr Voorhees, NJ 8043, US",
                "Guarantor_Phone": "N/A",
            },
            {
                "Plan": "PROGRESSIVE AUTOINSURANCE MOTORVEHICLE",
                "Claim_Address": "PO BOX 2930, CLINTON, IA 52733",
                "Claims_Phone": "+1-855-243-1331",
                "Policy_Number": "80001101 ",
                "Group_Number": "80001101",
                "Relation": "Self",
                "Employer": "N/A",
                "Guarantor_Name": "Michael Dershem",
                "Guarantor_DoB": "07/5/1963",
                "Guarantor_Address": "22 Oak Ridge Drive 22 Oak Ridge Dr Voorhees, NJ 8043, US",
                "Guarantor_Phone": "N/A",
            },
            {
                "Plan": "HORIZON BLUE CROSS",
                "Claim_Address": "P.O Box 1609, Newark, NJ 07101",
                "Claims_Phone": "+1-800-624-1110",
                "Policy_Number": "50000204 ",
                "Group_Number": "50000204",
                "Relation": "Self",
                "Employer": "N/A",
                "Guarantor_Name": "Michael Dershem",
                "Guarantor_DoB": "07/5/1963",
                "Guarantor_Address": "22 Oak Ridge Drive 22 Oak Ridge Dr Voorhees, NJ 8043, US",
                "Guarantor_Phone": "N/A",
            },
        ],
        "PROBLEMS": "Unknown Problems",
        "RESULTS": [
            {
                "Test_Name": "CT Head or Brain without Contrast",
                "Collected": "10/11/2019 12:38 AM",
                "Sub_Test": [
                    {
                        "Test": "IMP",
                        "Values_Unit": "Unremarkable CT of the brain",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                    {
                        "Test": "NAR",
                        "Values_Unit": "HISTORY: Minor head trauma COMPARISON: There are no prior relevant studies available at this time. TECHNIQUE: Helical CT scans from the skull base through the vertex. Images reformatted coronal. Automated dose control measures were utilized. FINDINGS: Brain and dura: There is no evident mass, hemorrhage, recent infarct or extra-axial collection. There is no acute or significant focal intracranial abnormality. Skull: There is no significant skull or scalp abnormality identified. Sinuses and Orbits: The paranasal sinuses and mastoid air cells are clear. Minimal left preorbital soft tissue swelling is suggested. There is no orbit lesion appreciated.",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                    {
                        "Test": "PXN ",
                        "Values_Unit": "Roberts, David A, MD - 10/10/2019, Formatting of this note might be different from the original. HISTORY: Minor head trauma COMPARISON: There are no prior relevant studies available at this time. TECHNIQUE: Helical CT scans from the skull base through the vertex., Images reformatted coronal. Automated dose control measures were utilized. FINDINGS: Brain and dura: There is no evident mass, hemorrhage, recent infarct or extra-axial collection. There is no acute or significant focal, intracranial abnormality. Skull: There is no significant skull or scalp abnormality identified. Sinuses and Orbits: The paranasal sinuses and mastoid air cells are, clear. Minimal left preorbital soft tissue swelling is suggested. There is no, orbit lesion appreciated. IMPRESSION: Unremarkable CT of the brain.",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                    {
                        "Test": "N/A",
                        "Values_Unit": "7",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                ],
            },
            {
                "Test_Name": "CT Facial Bones without Contrast",
                "Collected": "10/11/2019 12:47 AM",
                "Sub_Test": [
                    {
                        "Test": "IMP",
                        "Values_Unit": "Left nasal fracture.",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                    {
                        "Test": "NAR",
                        "Values_Unit": "HISTORY: Left-sided facial trauma with headache COMPARISON: There are no prior relevant studies available.. TECHNIQUE: Helically acquired thin section axial CT scans were performed with coronal images reformatted from the axial data set. Automated dose control measures were utilized. FINDINGS: There is a minimally displaced/depressed fracture of the left nasal bone resulting in cortical offset measuring 1 mm. No other facial fracture is seen. There is mild left preorbital soft tissue swelling. The globes and orbits are within normal limits; no retrobulbar hemorrhage. No sinus air-fluid level or hemorrhage is identified. There is mild mucosal thickening in the inferior right maxillary sinus and within the ethmoid air cells.",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                    {
                        "Test": "PXN ",
                        "Values_Unit": "Roberts, David A, MD - 10/10/2019, Formatting of this note might be different from the original. HISTORY: Left-sided facial trauma with headache COMPARISON: There are no prior relevant studies available.. TECHNIQUE: Helically acquired thin section axial CT scans were performed, with coronal images reformatted from the axial data set. Automated dose, control measures were utilized. FINDINGS: There is a minimally displaced/depressed fracture of the left nasal bone resulting in cortical offset measuring 1 mm. No other facial fracture is, seen. There is mild left preorbital soft tissue swelling. The globes and orbits, are within normal limits; no retrobulbar hemorrhage. No sinus air-fluid level, or hemorrhage is identified. There is mild mucosal thickening in the inferior, right maxillary sinus and within the ethmoid air cells. IMPRESSION: Left nasal fracture.",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                    {
                        "Test": "N/A",
                        "Values_Unit": "7",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                ],
            },
            {
                "Test_Name": "CT Cervical Spine without Contrast",
                "Collected": " 10/11/2019 12:49 AM",
                "Sub_Test": [
                    {
                        "Test": "IMP",
                        "Values_Unit": "No cervical fracture or dislocation. Degenerative changes, most prominent at C5-6",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                    {
                        "Test": "NAR",
                        "Values_Unit": "HISTORY: Trauma COMPARISON: There are no prior relevant studies available. TECHNIQUE: Axial images were obtained from the skull base to the thoracic inlet. Sagittal and coronal reformatted images were generated and reviewed. Automated dose control measures were utilized. FINDINGS: The vertebral bodies are normally aligned. The vertebral body heights are preserved. There is no evidence of acute fracture. No focal suspicious osseous lesion is identified. Evaluation of the spinal canal and spinal cord is intrinsically limited on this modality. Disc space levels: There is severe discogenic narrowing and moderate reactive endplate spurring at C5-6. There is milder discogenic narrowing/spurring at C4-5. There is prominent right-sided uncovertebral disease at C3-4 resulting in bony foraminal stenosis. Areas of mild bilateral diffuse facet arthrosis are present. The paravertebral soft tissues are unremarkable. Visualized portions of the brain and calvarium are unremarkable. The visualized lung apices are clear.",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                    {
                        "Test": "PXN ",
                        "Values_Unit": "Roberts, David A, MD - 10/10/2019, Formatting of this note might be different from the original. HISTORY: Trauma COMPARISON: There are no prior relevant studies available. TECHNIQUE: Axial images were obtained from the skull base to the, thoracic inlet. Sagittal and coronal reformatted images were generated and, reviewed. Automated dose control measures were utilized. FINDINGS: The vertebral bodies are normally aligned. The vertebral body heights, are preserved. There is no evidence of acute fracture. No focal suspicious osseous, lesion is identified. Evaluation of the spinal canal and spinal cord is intrinsically limited on, this modality. Disc space levels: There is severe discogenic narrowing and moderate, reactive endplate spurring at C5-6. There is milder discogenic narrowing/spurring, at C4-5. There is prominent right-sided uncovertebral disease at C3-4, resulting in bony foraminal stenosis. Areas of mild bilateral diffuse facet arthrosis, are present. The paravertebral soft tissues are unremarkable. Visualized portions of the brain and calvarium are unremarkable. The visualized lung apices are clear. IMPRESSION: No cervical fracture or dislocation. Degenerative changes, most prominent at C5-6.",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                    {
                        "Test": "N/A",
                        "Values_Unit": "7",
                        "Interpretation": "Normal",
                        "Reference_Range": "N/A",
                    },
                ],
            },
        ],
        "ALLERGIES_ADVERSE_REACTIONS_ALERTS": "No known allergies and adverse reactions",
        "MEDICATIONS": "No administered medications reported",
        "VITAL_SIGNS": [
            {
                "Date": "10/10/2019 10:59 PM ",
                "Vital": "Temperature",
                "Result": "36.5 Cel",
                "Comment": "N/A",
            },
            {
                "Date": "10/10/2019 11:00 PM ",
                "Vital": "Body Weight ",
                "Result": "77.111 kg",
                "Comment": "N/A",
            },
            {
                "Date": "10/10/2019 11:00 PM ",
                "Vital": [
                    "Oxygen Saturation",
                    "Respiratory Rate",
                    "Heart Rate",
                    "Blood Preasure Systolic",
                    "Blood Preasure Diastolic",
                ],
                "Result": ["99%", "16/min", "63 /min", "148 mm[Hg]", "84 mm[Hg]"],
                "Comment": "N/A",
            },
        ],
        "PROCEDURES": [
            {
                "Procedure": "HC CT CERVICAL SPINE W/O CONTRAST",
                "Date": "10/11/2019 12:38 AM",
                "Notes": "N/A",
                "Body_Site": "N/A",
                "Specimen": "N/A",
                "Indications": "N/A",
                "Status": "Completed",
            },
            {
                "Procedure": "HC CT FACIAL BONES W/O CONTRAST",
                "Date": "10/11/2019 12:38 AM",
                "Notes": "N/A",
                "Body_Site": "N/A",
                "Specimen": "N/A",
                "Indications": "N/A",
                "Status": "Completed",
            },
            {
                "Procedure": "HC CT T HEAD OR BRAIN W/O CONTRAST",
                "Date": "10/11/2019 12:38 AM",
                "Notes": "N/A",
                "Body_Site": "N/A",
                "Specimen": "N/A",
                "Indications": "N/A",
                "Status": "Completed",
            },
        ],
        "SOCIAL_HISTORY": [
            {
                "Element": "Tobacco smoking status NHIS",
                "Description": "Never smoked tobacco",
                "Date": "10/10/2019",
                "Comment": "N/A",
            },
            {
                "Element": "Tobacco use and exposure ",
                "Description": "Smokeless tobacco non-user ",
                "Date": "10/10/2019",
                "Comment": "N/A",
            },
            {
                "Element": "Alcohol intake",
                "Description": "Current drinker of alcohol (finding) ",
                "Date": "10/10/2019",
                "Comment": "N/A",
            },
            {
                "Element": "History SDOH Alcohol Comment",
                "Description": "Socially ",
                "Date": "10/10/2019",
                "Comment": "N/A",
            },
            {
                "Element": "Sex Assigned At Birth ",
                "Description": "Not on file  ",
                "Date": "07/05/1963",
                "Comment": "N/A",
            },
            {
                "Element": "Tobacco smoking status NHIS",
                "Description": "Tobacco smoking consumption unknown",
                "Date": "N/A",
                "Comment": "N/A",
            },
        ],
        "ENCOUNTERS": [
            {
                "Type": "Emergency",
                "CPT_Code": "N/A",
                "Date": "10/10/2019 07:01 PM - 10/10/2019 09:11 PM",
                "Location": "Voorhees Emergency Department 100 Bowman Drive, Voorhees, NJ 08043",
                "Provider": "Douglas Stranges",
                "Indications": "81639003 : null",
                "Comments": "Closed fracture of nasal bone, initial encounter (Primary Dx)",
            },
            {
                "Type": "Office Visit ",
                "CPT_Code": "MG1030",
                "Date": "10/14/2019 07:45 AM - 10/14/2019 08:42 AM ",
                "Location": "Otorhinolaryngology - PMWS 800 Walnut Street, Floor 18, Philadelphia, PA 19107",
                "Provider": "James Kearney",
                "Indications": "81639003 : null",
                "Comments": "Closed fracture of nasal bone, initial encounter (Primary Dx)",
            },
        ],
        "PLAN_OF_CARE": [
            {"Date": "07/05/1974", "Activity": "TDAP Vaccine"},
            {
                "Date": "07/05/1981",
                "Activity": [
                    "Annual BMI Assessment",
                    "Hepatitis C Screening",
                    "Provide Tobacco Cessation Counseling",
                    "Td Vaccine",
                    "Tobacco Screening",
                ],
            },
            {
                "Date": "07/05/2013",
                "Activity": ["Colon Cancer Screening", "Zoster Vaccines (1 of 2)"],
            },
            {"Date": "09/01/2022", "Activity": "Influenza Vaccine (Season Ended)"},
            {
                "Date": "07/05/2028",
                "Activity": "Pneumococcal PPSV23 Low Risk Adult (1 of 2 - PCV13)",
            },
            {
                "Date": "07/05/1963",
                "Activity": [
                    "COLONOSCOPY",
                    "COMBO COLO Topic NEW",
                    "FIT/FOBT Q 1 Year",
                    "HEPATITIS C SCREENING",
                ],
            },
            {"Date": "07/05/1978", "Activity": "HIV SCREENING ONCE"},
            {"Date": "07/05/1981", "Activity": ["COLOGUARD Q 3 YEARS", "LIPIDS"]},
            {"Date": "07/05/1982", "Activity": "DTAP/TDAP/TD (1 - Tdap)"},
            {"Date": "07/05/2008", "Activity": "Diabetes Screening"},
            {
                "Date": "07/05/2013",
                "Activity": [
                    "PSA COUNSELING",
                    "ZOSTER VACCINES (1 of 2 - RZV, Shingrix)",
                ],
            },
            {"Date": "09/01/2021", "Activity": "INFLUENZA (#1)"},
        ],
        "DOCUMENT_INFORMATION": {
            "Document_Identifier": "98b88f97-66e7-45ca-96c6-a647ecebbc0d OID: 1.3.6.1.4.1.52618.1.4",
            "Document_Created": "04/20/2022, 15:33",
        },
    }
    return Report
