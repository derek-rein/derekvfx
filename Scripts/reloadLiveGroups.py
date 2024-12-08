import nuke

def reload_all_live_groups():
    """
    Reloads the content of all Live Group nodes in the current Nuke script.
    """
    live_group_nodes = [node for node in nuke.allNodes() if node.Class() == "LiveGroup"]

    if not live_group_nodes:
        nuke.message("No Live Group nodes found in the script.")
        return

    for live_group in live_group_nodes:
        try:
            live_group['reload_script'].execute()  # Clicks the 'Reload' button
            nuke.tprint(f"Reloaded Live Group: {live_group.name()}")
        except Exception as e:
            nuke.tprint(f"Failed to reload Live Group {live_group.name()}: {e}")

    nuke.message("All Live Group nodes have been reloaded.")

# Call the function
reload_all_live_groups()