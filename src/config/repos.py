from typing import Dict, List

ORGANIZATION = "AlmSmartDoctor"

REPOS: Dict[str, List[str]] = {
    "C#": [
        "SmartDoctorCrm", "AlmightyClaim", "Almighty", "SmartDoctorAgent",
        "CustImageManager", "WebService", "CloudBackup", "SmartChartServer",
        "SmartDocument", "NHISMediConn", "SmartPenChart", "smart-doctor-pay-server",
        "SmartNcCapture", "ProcessManagement", "SmartMQ", "SmartInterview",
        "Common_SmartDoctor", "AlmSmartCall", "CashDocAgent"
    ],
    "Backend": [
        "smartdoctor-api", "reservation-platform-api", "unite-api",
        "Yeogiya-API-Server", "cashdoc-hospital-event-prisma", "quiz-api",
        "cash-review-api", "SmartSurvey-API-Server", "message-cron",
        "smart-inquiry", "cashdoc-serverless"
    ],
    "Frontend": [
        "cash-review", "Yeogiya-User-Next", "cashdoc-webview",
        "procedure-allocation", "SmartSurvey-Client", "smart-waiting",
        "auto-receipt-web", "reservation-platform-front", "smart-web-scheduler",
        "almighty-smart-front", "smart-inquiry", "smart-doctor-amplify-master-web",
        "cashdoc-webview-search-hospital"
    ],
    "Android": [
        "SmartDoctorPay_Android", "CashDocAndroid", "SmartChart_Android",
        "smart-auto-receipt-android", "Common_Android", "Logger_Android"
    ]
}
