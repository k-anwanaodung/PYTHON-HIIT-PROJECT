import json
import os
from datetime import datetime
from instagrapi import Client
from pathlib import Path

class InstagramUnfollowersBot:
    def __init__(self):
        self.client = Client()
        self.followers_file = "followers_history.json"
        self.unfollowers_file = "unfollowers_report.json"

    def login(self, username, password):
        """Login to Instagram"""
        try:
            self.client.login(username, password)
            print(f"✓ Successfully logged in as {username}")
            return True
        except Exception as e:
            print(f"✗ Login failed: {e}")
            return False

    def get_followers(self):
        """Get current followers list"""
        try:
            print("📥 Fetching your followers... (this may take a while)")
            followers = self.client.user_followers(self.client.user_id)
            followers_list = [{"username": user.username, "user_id": user.pk} for user in followers]
            return followers_list
        except Exception as e:
            print(f"✗ Error fetching followers: {e}")
            return None

    def save_followers(self, followers_list):
        """Save current followers to file"""
        try:
            history = {}
            if os.path.exists(self.followers_file):
                with open(self.followers_file, 'r') as f:
                    history = json.load(f)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history[timestamp] = {
                "count": len(followers_list),
                "followers": followers_list
            }

            with open(self.followers_file, 'w') as f:
                json.dump(history, f, indent=2)

            print(f"✓ Saved {len(followers_list)} followers to history")
            return True
        except Exception as e:
            print(f"✗ Error saving followers: {e}")
            return False

    def find_unfollowers(self):
        """Find users who unfollowed you"""
        try:
            if not os.path.exists(self.followers_file):
                print("✗ No previous follower data found. This is your first check!")
                print("  Please run the bot again tomorrow to find unfollowers.")
                return []

            with open(self.followers_file, 'r') as f:
                history = json.load(f)

            # Get the last two entries
            timestamps = sorted(history.keys())
            if len(timestamps) < 2:
                print("✗ Need at least 2 data points to find unfollowers.")
                print(f"  Current data points: {len(timestamps)}")
                return []

            previous_followers = set((u["username"]) for u in history[timestamps[-2]]["followers"])
            current_followers = set((u["username"]) for u in history[timestamps[-1]]["followers"])

            unfollowers = list(previous_followers - current_followers)

            return unfollowers
        except Exception as e:
            print(f"✗ Error finding unfollowers: {e}")
            return []

    def save_unfollowers_report(self, unfollowers):
        """Save unfollowers report"""
        try:
            report = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "count": len(unfollowers),
                "unfollowers": unfollowers
            }

            # Keep last 20 reports
            all_reports = []
            if os.path.exists(self.unfollowers_file):
                with open(self.unfollowers_file, 'r') as f:
                    all_reports = json.load(f)

            all_reports.append(report)
            if len(all_reports) > 20:
                all_reports = all_reports[-20:]

            with open(self.unfollowers_file, 'w') as f:
                json.dump(all_reports, f, indent=2)

            return True
        except Exception as e:
            print(f"✗ Error saving report: {e}")
            return False

    def display_unfollowers(self, unfollowers):
        """Display unfollowers in a nice format"""
        if not unfollowers:
            print("\n✓ No new unfollowers detected! 👍")
            return

        print(f"\n⚠️  UNFOLLOWERS DETECTED ({len(unfollowers)}):")
        print("=" * 50)
        for i, user in enumerate(unfollowers, 1):
            print(f"{i}. @{user}")
        print("=" * 50)

    def get_stats(self):
        """Display follower statistics"""
        try:
            if not os.path.exists(self.followers_file):
                print("✗ No data yet")
                return

            with open(self.followers_file, 'r') as f:
                history = json.load(f)

            timestamps = sorted(history.keys())
            first_check = history[timestamps[0]]
            latest_check = history[timestamps[-1]]

            print("\n📊 STATISTICS:")
            print("=" * 50)
            print(f"First check: {timestamps[0]} ({first_check['count']} followers)")
            print(f"Latest check: {timestamps[-1]} ({latest_check['count']} followers)")
            print(f"Total checks: {len(timestamps)}")

            if len(timestamps) > 1:
                change = latest_check['count'] - first_check['count']
                if change > 0:
                    print(f"Change: +{change} followers")
                else:
                    print(f"Change: {change} followers")
            print("=" * 50)
        except Exception as e:
            print(f"✗ Error getting stats: {e}")

    def run(self):
        """Main bot workflow"""
        print("\n" + "="*50)
        print("📱 INSTAGRAM UNFOLLOWERS CHECKER BOT")
        print("="*50 + "\n")

        # Get credentials
        username = input("Enter your Instagram username: ").strip()
        password = input("Enter your Instagram password: ").strip()

        # Login
        if not self.login(username, password):
            return

        # Get followers
        followers = self.get_followers()
        if not followers:
            return

        # Save followers
        self.save_followers(followers)

        # Find unfollowers
        unfollowers = self.find_unfollowers()

        # Display results
        self.display_unfollowers(unfollowers)

        # Save report
        if unfollowers:
            self.save_unfollowers_report(unfollowers)

        # Show stats
        self.get_stats()

        print("\n✓ Bot execution completed!")


if __name__ == "__main__":
    bot = InstagramUnfollowersBot()
    bot.run()
