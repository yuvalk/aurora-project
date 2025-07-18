#!/usr/bin/env python3
"""
Aurora Activity Graph Generator
Creates text-based visualizations of aurora data
"""

import random
import datetime

class AuroraGraph:
    def __init__(self):
        self.colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'yellow': '\033[93m',
            'cyan': '\033[96m',
            'purple': '\033[95m',
            'white': '\033[97m',
            'reset': '\033[0m'
        }
        
    def generate_sample_data(self, days=14):
        """Generate sample aurora activity data"""
        data = []
        base_activity = 3.0
        
        for i in range(days):
            # Simulate natural variations
            daily_change = random.uniform(-1.0, 1.5)
            base_activity = max(0.5, min(8.5, base_activity + daily_change))
            
            # Add some realistic spikes (solar storms)
            if random.random() < 0.15:  # 15% chance of storm
                base_activity = min(9.0, base_activity + random.uniform(2.0, 4.0))
            
            date = datetime.date.today() - datetime.timedelta(days=days-1-i)
            data.append({
                'date': date,
                'kp_index': round(base_activity, 1),
                'activity_level': self.get_activity_level(base_activity)
            })
            
        return data
    
    def get_activity_level(self, kp):
        """Convert KP index to activity level"""
        if kp < 2:
            return "Quiet"
        elif kp < 3:
            return "Unsettled"
        elif kp < 4:
            return "Active"
        elif kp < 5:
            return "Minor Storm"
        elif kp < 6:
            return "Moderate Storm"
        elif kp < 7:
            return "Strong Storm"
        elif kp < 8:
            return "Severe Storm"
        else:
            return "Extreme Storm"
    
    def create_bar_chart(self, data):
        """Create a horizontal bar chart of aurora activity"""
        print(self.colors['cyan'] + "📊 AURORA ACTIVITY - PAST 14 DAYS 📊" + self.colors['reset'])
        print(self.colors['white'] + "=" * 50 + self.colors['reset'])
        print()
        
        # Header
        print(f"{'Date':<12} {'KP':<4} {'Activity':<15} {'Graph':<20}")
        print("-" * 55)
        
        for day in data:
            date_str = day['date'].strftime("%m-%d")
            kp_val = day['kp_index']
            activity = day['activity_level']
            
            # Create visual bar
            bar_length = int(kp_val * 2)  # Scale for visibility
            if kp_val < 2:
                bar_color = self.colors['green']
                bar_char = '█'
            elif kp_val < 4:
                bar_color = self.colors['yellow']
                bar_char = '█'
            elif kp_val < 6:
                bar_color = self.colors['red']
                bar_char = '█'
            else:
                bar_color = self.colors['purple']
                bar_char = '█'
                
            bar = bar_color + bar_char * bar_length + self.colors['reset']
            
            print(f"{date_str:<12} {kp_val:<4} {activity:<15} {bar} {kp_val}")
        
        print()
        print(self.colors['green'] + "🟢 Quiet/Unsettled  " + self.colors['reset'] + 
              self.colors['yellow'] + "🟡 Active  " + self.colors['reset'] + 
              self.colors['red'] + "🔴 Storm  " + self.colors['reset'] + 
              self.colors['purple'] + "🟣 Severe+" + self.colors['reset'])
    
    def create_line_graph(self, data):
        """Create a simple ASCII line graph"""
        print("\n" + self.colors['blue'] + "📈 KP INDEX TREND LINE 📈" + self.colors['reset'])
        print(self.colors['white'] + "=" * 40 + self.colors['reset'])
        
        # Scale values for display
        max_kp = max(day['kp_index'] for day in data)
        min_kp = min(day['kp_index'] for day in data)
        
        # Create grid
        height = 10
        width = len(data)
        
        print(f"\nKP Range: {min_kp:.1f} - {max_kp:.1f}")
        print()
        
        # Y-axis labels and graph
        for row in range(height, 0, -1):
            kp_level = (row / height) * 9  # Scale to 0-9
            print(f"{kp_level:4.1f} |", end="")
            
            for i, day in enumerate(data):
                scaled_kp = (day['kp_index'] / 9) * height
                if abs(scaled_kp - row) < 0.8:
                    if day['kp_index'] < 3:
                        print(self.colors['green'] + "●" + self.colors['reset'], end="")
                    elif day['kp_index'] < 5:
                        print(self.colors['yellow'] + "●" + self.colors['reset'], end="")
                    else:
                        print(self.colors['red'] + "●" + self.colors['reset'], end="")
                else:
                    print(" ", end="")
            print()
        
        # X-axis
        print("     " + "-" * width)
        print("     ", end="")
        for i, day in enumerate(data):
            if i % 2 == 0:  # Show every other date
                print(day['date'].strftime("%m/%d")[2:], end="")
            else:
                print("  ", end="")
        print()
    
    def create_statistics_summary(self, data):
        """Create a summary of aurora statistics"""
        print("\n" + self.colors['purple'] + "📊 AURORA STATISTICS SUMMARY 📊" + self.colors['reset'])
        print(self.colors['white'] + "=" * 35 + self.colors['reset'])
        
        kp_values = [day['kp_index'] for day in data]
        
        avg_kp = sum(kp_values) / len(kp_values)
        max_kp = max(kp_values)
        min_kp = min(kp_values)
        
        # Count activity levels
        activity_counts = {}
        for day in data:
            level = day['activity_level']
            activity_counts[level] = activity_counts.get(level, 0) + 1
        
        storm_days = sum(1 for kp in kp_values if kp >= 5)
        active_days = sum(1 for kp in kp_values if kp >= 3)
        
        print(f"\n📊 KP Index Statistics:")
        print(f"   Average KP: {avg_kp:.1f}")
        print(f"   Maximum KP: {max_kp:.1f}")
        print(f"   Minimum KP: {min_kp:.1f}")
        
        print(f"\n⚡ Activity Summary:")
        print(f"   Storm Days (KP≥5): {storm_days}/14 days ({storm_days/14*100:.0f}%)")
        print(f"   Active Days (KP≥3): {active_days}/14 days ({active_days/14*100:.0f}%)")
        
        print(f"\n🎯 Best Viewing Chances:")
        excellent_days = sum(1 for kp in kp_values if kp >= 4)
        good_days = sum(1 for kp in kp_values if kp >= 3)
        
        print(f"   Excellent (KP≥4): {excellent_days} days")
        print(f"   Good (KP≥3): {good_days} days")
        
        if max_kp >= 6:
            print(f"\n🌟 Highlights:")
            print(f"   Peak activity reached {max_kp:.1f} - {self.get_activity_level(max_kp)}!")
            print(f"   Aurora likely visible as far south as central US!")

def main():
    aurora_graph = AuroraGraph()
    
    # Generate sample data
    data = aurora_graph.generate_sample_data(14)
    
    # Create visualizations
    aurora_graph.create_bar_chart(data)
    aurora_graph.create_line_graph(data)
    aurora_graph.create_statistics_summary(data)
    
    print(f"\n{aurora_graph.colors['cyan']}✨ Aurora data visualization complete! ✨{aurora_graph.colors['reset']}")
    print(f"{aurora_graph.colors['green']}Perfect for planning your next aurora hunting adventure! 🌌{aurora_graph.colors['reset']}")

if __name__ == "__main__":
    main()