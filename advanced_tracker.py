#!/usr/bin/env python3
"""
Q-AVIOGEN Advanced Daily Tracker
Complete commercialization tracking with demo, freemium, and payment systems
"""

import json
import os
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import sys

class QAVIOGENAdvancedTracker:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.data_file = self.project_root / "advanced_tracker_data.json"
        self.start_date = datetime.now()
        self.load_data()
        
    def load_data(self):
        """Load or initialize tracking data"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                # Convert string dates back to datetime
                self.start_date = datetime.fromisoformat(self.data["start_date"])
        else:
            self.data = self.initialize_data()
            self.save_data()
    
    def save_data(self):
        """Save tracking data"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def initialize_data(self):
        """Initialize comprehensive tracking data"""
        return {
            "project": "Q-AVIOGEN Complete Commercialization",
            "start_date": self.start_date.isoformat(),
            "target_revenue_month1": 15000,
            "current_revenue": 0,
            
            # Core KPIs
            "kpis": {
                "website_visitors": 0,
                "demo_uses": 0,
                "demo_completions": 0,
                "app_registrations": 0,
                "free_signups": 0,
                "paid_conversions": 0,
                "monthly_recurring_revenue": 0,
                "customer_acquisition_cost": 0,
                "lifetime_value": 0
            },
            
            # Freemium Funnel
            "freemium": {
                "free_users": 0,
                "free_active_users": 0,
                "base_plan_users": 0,
                "plus_plan_users": 0,
                "pro_plan_users": 0,
                "enterprise_inquiries": 0,
                "free_to_paid_conversion_rate": 0,
                "average_time_to_upgrade_days": 0,
                "monthly_churn_rate": 0
            },
            
            # Marketing Metrics
            "marketing": {
                "linkedin_engagement": 0,
                "twitter_engagement": 0,
                "email_open_rate": 0,
                "email_click_rate": 0,
                "demo_completion_rate": 0,
                "app_retention_day7": 0,
                "app_retention_day30": 0,
                "video_views": 0,
                "press_mentions": 0
            },
            
            # Revenue Breakdown
            "revenue_streams": {
                "base_plan_mrr": 0,
                "plus_plan_mrr": 0,
                "pro_plan_mrr": 0,
                "enterprise_deals": 0,
                "one_time_payments": 0,
                "consulting_revenue": 0
            },
            
            # Daily Progress
            "daily_progress": {},
            
            # Launch Assets Status
            "assets": {
                "landing_page": True,
                "demo_interactive": True,
                "freemium_app": True,
                "payment_system": False,
                "video_marketing": False,
                "email_automation": False,
                "analytics_setup": False,
                "social_media": False
            },
            
            # Goals and Milestones
            "milestones": {
                "first_demo_use": False,
                "first_signup": False,
                "first_payment": False,
                "100_visitors": False,
                "50_signups": False,
                "10_paid_users": False,
                "1000_eur_mrr": False,
                "5000_eur_mrr": False,
                "partner_signed": False,
                "press_coverage": False
            }
        }
    
    def get_current_day(self):
        """Get current day of the campaign"""
        return (datetime.now() - self.start_date).days + 1
    
    def display_header(self):
        """Display dashboard header"""
        day = self.get_current_day()
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        print("\n" + "="*100)
        print(f"🚀 Q-AVIOGEN ADVANCED COMMERCIALIZATION TRACKER - DAY {day}/30")
        print(f"📅 {today}")
        print("="*100)
    
    def display_revenue_dashboard(self):
        """Display revenue progress"""
        current = self.data["current_revenue"]
        target = self.data["target_revenue_month1"]
        progress = (current / target * 100) if target > 0 else 0
        
        print(f"\n💰 REVENUE DASHBOARD:")
        print(f"   Current Revenue: €{current:,.2f}")
        print(f"   Monthly Target:  €{target:,.2f}")
        print(f"   Progress: {progress:.1f}% {self.get_status_emoji(progress, [25, 50, 75])}")
        
        self.draw_progress_bar(progress, width=60)
        
        # MRR Breakdown
        mrr = self.data["revenue_streams"]
        total_mrr = sum([mrr["base_plan_mrr"], mrr["plus_plan_mrr"], mrr["pro_plan_mrr"]])
        
        if total_mrr > 0:
            print(f"\n   📈 Monthly Recurring Revenue: €{total_mrr:,.2f}")
            print(f"      Base Plan (€49): €{mrr['base_plan_mrr']:,.2f}")
            print(f"      Plus Plan (€149): €{mrr['plus_plan_mrr']:,.2f}")
            print(f"      Pro Plan (€299): €{mrr['pro_plan_mrr']:,.2f}")
    
    def display_funnel_metrics(self):
        """Display conversion funnel"""
        kpis = self.data["kpis"]
        freemium = self.data["freemium"]
        
        print(f"\n📊 CONVERSION FUNNEL:")
        print(f"   🌐 Website Visitors: {kpis['website_visitors']:,}")
        print(f"   🎮 Demo Uses: {kpis['demo_uses']:,} ({self.calc_rate(kpis['demo_uses'], kpis['website_visitors'])}%)")
        print(f"   ✅ Demo Completions: {kpis['demo_completions']:,} ({self.calc_rate(kpis['demo_completions'], kpis['demo_uses'])}%)")
        print(f"   📝 App Registrations: {kpis['app_registrations']:,} ({self.calc_rate(kpis['app_registrations'], kpis['demo_completions'])}%)")
        print(f"   👥 Free Signups: {kpis['free_signups']:,}")
        print(f"   💳 Paid Conversions: {kpis['paid_conversions']:,} ({self.calc_rate(kpis['paid_conversions'], kpis['free_signups'])}%)")
        
        print(f"\n🎯 FREEMIUM BREAKDOWN:")
        total_users = freemium['free_users'] + freemium['base_plan_users'] + freemium['plus_plan_users'] + freemium['pro_plan_users']
        print(f"   👥 Total Users: {total_users:,}")
        if total_users > 0:
            print(f"   🆓 Free: {freemium['free_users']:,} ({freemium['free_users']/total_users*100:.1f}%)")
            print(f"   💼 Base: {freemium['base_plan_users']:,} ({freemium['base_plan_users']/total_users*100:.1f}%)")
            print(f"   ⭐ Plus: {freemium['plus_plan_users']:,} ({freemium['plus_plan_users']/total_users*100:.1f}%)")
            print(f"   🚀 Pro: {freemium['pro_plan_users']:,} ({freemium['pro_plan_users']/total_users*100:.1f}%)")
    
    def display_marketing_metrics(self):
        """Display marketing performance"""
        marketing = self.data["marketing"]
        
        print(f"\n📢 MARKETING PERFORMANCE:")
        print(f"   💼 LinkedIn Engagement: {marketing['linkedin_engagement']:,}")
        print(f"   🐦 Twitter Engagement: {marketing['twitter_engagement']:,}")
        print(f"   📧 Email Open Rate: {marketing['email_open_rate']:.1f}%")
        print(f"   🎬 Video Views: {marketing['video_views']:,}")
        print(f"   📰 Press Mentions: {marketing['press_mentions']:,}")
        print(f"   📱 App 7-day Retention: {marketing['app_retention_day7']:.1f}%")
        print(f"   📱 App 30-day Retention: {marketing['app_retention_day30']:.1f}%")
    
    def display_asset_status(self):
        """Display launch assets status"""
        assets = self.data["assets"]
        
        print(f"\n🔧 LAUNCH ASSETS STATUS:")
        for asset, status in assets.items():
            emoji = "✅" if status else "❌"
            name = asset.replace("_", " ").title()
            print(f"   {emoji} {name}")
    
    def display_milestones(self):
        """Display milestone achievements"""
        milestones = self.data["milestones"]
        achieved = sum(milestones.values())
        total = len(milestones)
        
        print(f"\n🏆 MILESTONES ({achieved}/{total} achieved):")
        for milestone, achieved in milestones.items():
            emoji = "✅" if achieved else "🎯"
            name = milestone.replace("_", " ").title()
            print(f"   {emoji} {name}")
    
    def display_daily_tasks(self):
        """Display today's strategic tasks"""
        day = self.get_current_day()
        tasks = self.get_daily_tasks(day)
        
        print(f"\n📋 TODAY'S STRATEGIC TASKS (DAY {day}):")
        for i, task in enumerate(tasks, 1):
            priority_emoji = {"high": "🔥", "medium": "📌", "low": "📝"}
            status_emoji = "✅" if task.get("completed", False) else "⭐"
            
            print(f"   {status_emoji} {priority_emoji.get(task.get('priority', 'medium'), '📌')} {task['task']}")
            if task.get("hours"):
                print(f"      ⏱️  Time: {task['hours']}h")
            if task.get("revenue_impact"):
                print(f"      💰 Revenue Impact: €{task['revenue_impact']}")
            if task.get("metric_impact"):
                print(f"      📊 KPI Impact: {task['metric_impact']}")
    
    def get_daily_tasks(self, day):
        """Get strategic tasks based on current day and progress"""
        # Base tasks for all days
        base_tasks = [
            {"task": "Monitor demo usage and optimize UX", "hours": 1, "priority": "high", "revenue_impact": 200},
            {"task": "Engage with prospects on LinkedIn", "hours": 1, "priority": "high", "revenue_impact": 300},
            {"task": "Analyze freemium conversion data", "hours": 0.5, "priority": "medium", "revenue_impact": 100},
            {"task": "Customer outreach and follow-ups", "hours": 2, "priority": "high", "revenue_impact": 500}
        ]
        
        # Phase-specific tasks
        if day <= 7:  # Launch week
            launch_tasks = [
                {"task": "Complete payment system integration", "hours": 3, "priority": "high", "revenue_impact": 2000},
                {"task": "Launch marketing video campaign", "hours": 2, "priority": "high", "revenue_impact": 1500},
                {"task": "Setup email automation sequences", "hours": 2, "priority": "medium", "revenue_impact": 800},
                {"task": "Configure advanced analytics", "hours": 1, "priority": "medium", "revenue_impact": 300}
            ]
            return launch_tasks + base_tasks[:2]
        
        elif day <= 14:  # Growth phase
            growth_tasks = [
                {"task": "Scale advertising campaigns", "hours": 2, "priority": "high", "revenue_impact": 1000},
                {"task": "Partner outreach (Boeing, Airbus)", "hours": 3, "priority": "high", "revenue_impact": 5000},
                {"task": "Content marketing optimization", "hours": 2, "priority": "medium", "revenue_impact": 400},
                {"task": "Customer success and retention", "hours": 2, "priority": "high", "revenue_impact": 800}
            ]
            return growth_tasks + base_tasks[:1]
        
        else:  # Scale phase
            scale_tasks = [
                {"task": "Enterprise sales calls", "hours": 4, "priority": "high", "revenue_impact": 3000},
                {"task": "Product feature development", "hours": 3, "priority": "medium", "revenue_impact": 1000},
                {"task": "Investor pitch preparation", "hours": 2, "priority": "medium", "revenue_impact": 0},
                {"task": "Team hiring and scaling", "hours": 2, "priority": "low", "revenue_impact": 0}
            ]
            return scale_tasks + base_tasks[:1]
    
    def calc_rate(self, numerator, denominator):
        """Calculate percentage rate"""
        return (numerator / denominator * 100) if denominator > 0 else 0
    
    def get_status_emoji(self, value, thresholds):
        """Get status emoji based on thresholds"""
        if value >= thresholds[2]:
            return "🟢"
        elif value >= thresholds[1]:
            return "🟡"
        elif value >= thresholds[0]:
            return "🟠"
        else:
            return "🔴"
    
    def draw_progress_bar(self, percentage, width=50):
        """Draw a progress bar"""
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        print(f"   [{bar}] {percentage:.1f}%")
    
    def display_quick_actions(self):
        """Display quick action menu"""
        print(f"\n⚡ QUICK ACTIONS:")
        print(f"   1. 🎮 Open Interactive Demo")
        print(f"   2. 📱 Open Freemium App")
        print(f"   3. 🌐 Open Landing Page")
        print(f"   4. 📊 Update Metrics")
        print(f"   5. 💰 Add Revenue")
        print(f"   6. ✅ Complete Task")
        print(f"   7. 🚀 Launch Campaign")
        print(f"   8. 📈 Analytics Report")
        print(f"   9. 🎯 Set Milestone")
        print(f"   0. Exit Tracker")
    
    def handle_actions(self):
        """Handle user actions"""
        while True:
            choice = input(f"\n🎯 Select action (0-9): ").strip()
            
            if choice == "0":
                print("\n🚀 Great progress today! Tomorrow brings new opportunities!")
                break
            elif choice == "1":
                self.open_demo()
            elif choice == "2":
                self.open_app()
            elif choice == "3":
                self.open_landing_page()
            elif choice == "4":
                self.update_metrics()
            elif choice == "5":
                self.add_revenue()
            elif choice == "6":
                self.complete_task()
            elif choice == "7":
                self.launch_campaign()
            elif choice == "8":
                self.analytics_report()
            elif choice == "9":
                self.set_milestone()
            else:
                print("❌ Invalid option. Please try again.")
    
    def open_demo(self):
        """Open interactive demo"""
        demo_path = self.project_root / "website" / "demo.html"
        if demo_path.exists():
            webbrowser.open(f"file://{demo_path}")
            print("🎮 Interactive demo opened!")
            
            # Update metrics
            self.data["kpis"]["demo_uses"] += 1
            self.data["marketing"]["demo_completion_rate"] = min(90, self.data["marketing"]["demo_completion_rate"] + 0.5)
            self.save_data()
        else:
            print("❌ Demo file not found. Please create demo.html first.")
    
    def open_app(self):
        """Open freemium app"""
        app_path = self.project_root / "website" / "app.html"
        if app_path.exists():
            webbrowser.open(f"file://{app_path}")
            print("📱 Freemium app opened!")
            
            # Update metrics
            self.data["kpis"]["app_registrations"] += 1
            self.data["marketing"]["app_retention_day7"] = min(85, self.data["marketing"]["app_retention_day7"] + 0.3)
            self.save_data()
        else:
            print("❌ App file not found. Please create app.html first.")
    
    def open_landing_page(self):
        """Open landing page"""
        landing_path = self.project_root / "website" / "index.html"
        if landing_path.exists():
            webbrowser.open(f"file://{landing_path}")
            print("🌐 Landing page opened!")
            
            # Update metrics
            self.data["kpis"]["website_visitors"] += 1
            self.save_data()
        else:
            print("❌ Landing page not found. Please create index.html first.")
    
    def update_metrics(self):
        """Update metrics interactively"""
        print("\n📊 UPDATE METRICS")
        print("Enter new values (press Enter to skip):")
        
        # Core KPIs
        kpis = [
            ("website_visitors", "🌐 Website Visitors"),
            ("demo_uses", "🎮 Demo Uses"),
            ("demo_completions", "✅ Demo Completions"),
            ("app_registrations", "📝 App Registrations"),
            ("free_signups", "👥 Free Signups"),
            ("paid_conversions", "💳 Paid Conversions")
        ]
        
        for key, label in kpis:
            current = self.data["kpis"][key]
            new_value = input(f"{label} (current: {current}): ").strip()
            if new_value:
                try:
                    self.data["kpis"][key] = int(new_value)
                except ValueError:
                    print(f"❌ Invalid value for {label}")
        
        # Freemium metrics
        print("\n🎯 FREEMIUM METRICS:")
        freemium_metrics = [
            ("free_users", "🆓 Free Users"),
            ("base_plan_users", "💼 Base Plan Users (€49/mo)"),
            ("plus_plan_users", "⭐ Plus Plan Users (€149/mo)"),
            ("pro_plan_users", "🚀 Pro Plan Users (€299/mo)")
        ]
        
        for key, label in freemium_metrics:
            current = self.data["freemium"][key]
            new_value = input(f"{label} (current: {current}): ").strip()
            if new_value:
                try:
                    self.data["freemium"][key] = int(new_value)
                    
                    # Update MRR automatically
                    if key == "base_plan_users":
                        self.data["revenue_streams"]["base_plan_mrr"] = int(new_value) * 49
                    elif key == "plus_plan_users":
                        self.data["revenue_streams"]["plus_plan_mrr"] = int(new_value) * 149
                    elif key == "pro_plan_users":
                        self.data["revenue_streams"]["pro_plan_mrr"] = int(new_value) * 299
                        
                except ValueError:
                    print(f"❌ Invalid value for {label}")
        
        self.save_data()
        print("✅ Metrics updated successfully!")
    
    def add_revenue(self):
        """Add revenue entry"""
        print("\n💰 ADD REVENUE")
        
        amount = input("Enter amount (€): ").strip()
        source = input("Revenue source: ").strip()
        type_revenue = input("Type (subscription/one-time/consulting): ").strip().lower()
        
        try:
            amount = float(amount)
            self.data["current_revenue"] += amount
            
            # Categorize revenue
            if type_revenue == "subscription" or "subscription" in source.lower():
                if "base" in source.lower():
                    self.data["revenue_streams"]["base_plan_mrr"] += amount
                elif "plus" in source.lower():
                    self.data["revenue_streams"]["plus_plan_mrr"] += amount
                elif "pro" in source.lower():
                    self.data["revenue_streams"]["pro_plan_mrr"] += amount
            elif type_revenue == "consulting":
                self.data["revenue_streams"]["consulting_revenue"] += amount
            else:
                self.data["revenue_streams"]["one_time_payments"] += amount
            
            # Update MRR
            total_mrr = (self.data["revenue_streams"]["base_plan_mrr"] + 
                        self.data["revenue_streams"]["plus_plan_mrr"] + 
                        self.data["revenue_streams"]["pro_plan_mrr"])
            self.data["kpis"]["monthly_recurring_revenue"] = total_mrr
            
            # Log the entry
            today = datetime.now().strftime("%Y-%m-%d")
            if today not in self.data["daily_progress"]:
                self.data["daily_progress"][today] = []
            
            self.data["daily_progress"][today].append({
                "type": "revenue",
                "amount": amount,
                "source": source,
                "revenue_type": type_revenue,
                "timestamp": datetime.now().isoformat()
            })
            
            self.save_data()
            print(f"✅ Added €{amount:.2f} from {source}")
            print(f"💰 Total Revenue: €{self.data['current_revenue']:.2f}")
            print(f"📈 Monthly MRR: €{total_mrr:.2f}")
            
            # Check milestones
            self.check_revenue_milestones()
            
        except ValueError:
            print("❌ Invalid amount")
    
    def check_revenue_milestones(self):
        """Check and update revenue milestones"""
        mrr = self.data["kpis"]["monthly_recurring_revenue"]
        revenue = self.data["current_revenue"]
        
        if revenue >= 1 and not self.data["milestones"]["first_payment"]:
            self.data["milestones"]["first_payment"] = True
            print("🎉 MILESTONE: First payment received!")
        
        if mrr >= 1000 and not self.data["milestones"]["1000_eur_mrr"]:
            self.data["milestones"]["1000_eur_mrr"] = True
            print("🎉 MILESTONE: €1,000 MRR achieved!")
        
        if mrr >= 5000 and not self.data["milestones"]["5000_eur_mrr"]:
            self.data["milestones"]["5000_eur_mrr"] = True
            print("🎉 MILESTONE: €5,000 MRR achieved!")
    
    def launch_campaign(self):
        """Launch marketing campaign"""
        campaigns = [
            ("social_media_blitz", "📱 Social Media Blitz", {"visitors": 300, "demos": 80, "signups": 25}),
            ("email_campaign", "📧 Email Marketing Campaign", {"visitors": 150, "demos": 45, "signups": 15}),
            ("influencer_outreach", "🤝 Influencer Outreach", {"visitors": 500, "demos": 120, "signups": 35}),
            ("pr_launch", "📰 PR and Press Release", {"visitors": 800, "demos": 200, "signups": 60}),
            ("partnership_announcement", "🤝 Partnership Announcement", {"visitors": 400, "demos": 100, "signups": 30}),
            ("video_marketing", "🎬 Video Marketing Push", {"visitors": 600, "demos": 180, "signups": 50})
        ]
        
        print("\n🚀 MARKETING CAMPAIGNS:")
        for i, (key, name, impact) in enumerate(campaigns, 1):
            print(f"   {i}. {name}")
        
        try:
            choice = int(input("Select campaign (1-6): ")) - 1
            if 0 <= choice < len(campaigns):
                key, name, impact = campaigns[choice]
                
                print(f"\n🚀 Launching: {name}")
                print("🎯 Expected impact:")
                for metric, value in impact.items():
                    print(f"   +{value} {metric}")
                
                confirm = input("\n✅ Confirm launch? (y/n): ").strip().lower()
                if confirm == 'y':
                    # Apply impact
                    self.data["kpis"]["website_visitors"] += impact["visitors"]
                    self.data["kpis"]["demo_uses"] += impact["demos"]
                    self.data["kpis"]["free_signups"] += impact["signups"]
                    self.data["freemium"]["free_users"] += impact["signups"]
                    
                    # Update marketing metrics
                    if "social" in key:
                        self.data["marketing"]["linkedin_engagement"] += impact["visitors"] // 2
                        self.data["marketing"]["twitter_engagement"] += impact["visitors"] // 3
                    elif "email" in key:
                        self.data["marketing"]["email_open_rate"] = min(35, self.data["marketing"]["email_open_rate"] + 2)
                    elif "video" in key:
                        self.data["marketing"]["video_views"] += impact["visitors"] * 2
                    elif "pr" in key:
                        self.data["marketing"]["press_mentions"] += 3
                    
                    self.save_data()
                    print(f"✅ {name} launched successfully!")
                    print("📊 Metrics updated with expected impact.")
                
        except (ValueError, IndexError):
            print("❌ Invalid selection")
    
    def analytics_report(self):
        """Generate analytics report"""
        print("\n📈 ANALYTICS REPORT")
        print("="*50)
        
        # Conversion funnel analysis
        kpis = self.data["kpis"]
        visitors = kpis["website_visitors"]
        demos = kpis["demo_uses"]
        signups = kpis["free_signups"]
        paid = kpis["paid_conversions"]
        
        print("🔍 CONVERSION ANALYSIS:")
        if visitors > 0:
            demo_rate = demos / visitors * 100
            print(f"   Visitor → Demo: {demo_rate:.1f}%")
            
            if demos > 0:
                signup_rate = signups / demos * 100
                print(f"   Demo → Signup: {signup_rate:.1f}%")
                
                if signups > 0:
                    paid_rate = paid / signups * 100
                    print(f"   Signup → Paid: {paid_rate:.1f}%")
                    
                    overall_rate = paid / visitors * 100
                    print(f"   Overall Conversion: {overall_rate:.2f}%")
        
        # Revenue analysis
        revenue_streams = self.data["revenue_streams"]
        total_mrr = revenue_streams["base_plan_mrr"] + revenue_streams["plus_plan_mrr"] + revenue_streams["pro_plan_mrr"]
        
        print(f"\n💰 REVENUE ANALYSIS:")
        print(f"   Monthly Recurring Revenue: €{total_mrr:,.2f}")
        print(f"   Annual Run Rate: €{total_mrr * 12:,.2f}")
        
        if paid > 0:
            arpu = total_mrr / paid
            print(f"   Average Revenue Per User: €{arpu:.2f}")
        
        # Growth metrics
        day = self.get_current_day()
        if day > 1:
            daily_growth = (visitors / day)
            print(f"\n📈 GROWTH METRICS:")
            print(f"   Daily Average Visitors: {daily_growth:.1f}")
            
            if total_mrr > 0:
                projected_monthly = total_mrr * (30 / day)
                print(f"   Projected Monthly MRR: €{projected_monthly:,.2f}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if demo_rate < 10:
            print("   🎯 Focus on improving demo conversion - optimize landing page")
        if signup_rate < 20:
            print("   🎯 Improve demo experience - reduce friction, add value")
        if paid_rate < 5:
            print("   🎯 Enhance freemium value proposition and upgrade prompts")
        if total_mrr < 1000:
            print("   🎯 Prioritize customer acquisition and retention")
    
    def set_milestone(self):
        """Set or update milestone"""
        milestones = self.data["milestones"]
        
        print("\n🎯 MILESTONES:")
        for i, (key, achieved) in enumerate(milestones.items(), 1):
            status = "✅" if achieved else "🎯"
            name = key.replace("_", " ").title()
            print(f"   {i}. {status} {name}")
        
        try:
            choice = int(input("Select milestone to mark achieved (1-{}): ".format(len(milestones)))) - 1
            keys = list(milestones.keys())
            
            if 0 <= choice < len(keys):
                key = keys[choice]
                if not milestones[key]:
                    milestones[key] = True
                    name = key.replace("_", " ").title()
                    print(f"🎉 Milestone achieved: {name}")
                    self.save_data()
                else:
                    print("✅ Milestone already achieved!")
            else:
                print("❌ Invalid selection")
                
        except ValueError:
            print("❌ Invalid input")
    
    def complete_task(self):
        """Mark task as complete"""
        day = self.get_current_day()
        tasks = self.get_daily_tasks(day)
        
        print(f"\n📋 TODAY'S TASKS:")
        for i, task in enumerate(tasks, 1):
            status = "✅" if task.get("completed", False) else "⭐"
            print(f"   {i}. {status} {task['task']}")
        
        try:
            choice = int(input("Select task to complete (1-{}): ".format(len(tasks)))) - 1
            if 0 <= choice < len(tasks):
                task = tasks[choice]
                task["completed"] = True
                
                print(f"✅ Task completed: {task['task']}")
                
                # Apply revenue impact
                if task.get("revenue_impact"):
                    impact = task["revenue_impact"] * 0.1  # 10% immediate impact
                    self.data["current_revenue"] += impact
                    print(f"💰 Revenue impact: €{impact:.2f}")
                
                self.save_data()
            else:
                print("❌ Invalid task number")
        except ValueError:
            print("❌ Invalid input")
    
    def run(self):
        """Main dashboard loop"""
        self.display_header()
        self.display_revenue_dashboard()
        self.display_funnel_metrics()
        self.display_marketing_metrics()
        self.display_asset_status()
        self.display_milestones()
        self.display_daily_tasks()
        self.display_quick_actions()
        self.handle_actions()

def main():
    """Main entry point"""
    print("🚀 Initializing Q-AVIOGEN Advanced Tracker...")
    tracker = QAVIOGENAdvancedTracker()
    tracker.run()

if __name__ == "__main__":
    main()
