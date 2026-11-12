# Opt-in bulk pose: each passenger reads only its own named matrix.
$execute unless data storage rpg:lucifer_p2 pose.$(part) run return 0
$data modify entity @s transformation set from storage rpg:lucifer_p2 pose.$(part)
data merge entity @s {start_interpolation:0,interpolation_duration:1}
