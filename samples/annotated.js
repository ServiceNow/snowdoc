function isTableExtended(parent, child){
    gs.include("j2js");
    var tu = new TableUtils(parent);
    if(tu.tableExists() && tu.hasExtensions()){
        var tableArrayList = tu.getTableExtensions();
        var tableArray = j2js(tableArrayList);
        if(tableArray.indexOf(child) > -1){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}

// TODO: Could not automatically inject the following doc block:
/**
 * @class TableExtensionUtils
 * @classdesc Utility for checking table extension relationships.
 *
 * This utility provides functionality to determine if one table is an extension of another.
 * It leverages ServiceNow's TableUtils API to check the extension relationship between parent
 * and child tables, which is useful for inheritance-based validations and operations.
 *
 * @author Auto-Generated
 * @version 1.0.0
 */

// TODO: Could not automatically inject the following doc block:
/**
     * @constructor
     * @description Initialise the TableExtensionUtils class
     */

// TODO: Could not automatically inject the following doc block:
/**
     * Checks if a child table extends a parent table
     * 
     * @param {string} parent - The name of the potential parent table
     * @param {string} child - The name of the potential child table
     * @returns {boolean} True if child extends parent, false otherwise
     */