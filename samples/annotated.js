/**
 * Determines if a child table extends a parent table
 * 
 * @param {string} parent - The name of the potential parent table
 * @param {string} child - The name of the potential child table
 * @returns {boolean} True if child extends parent, false otherwise
 */
function isTableExtended(parent, child){
    gs.include("j2js");
    /**
     * @class TableExtensionUtils
     * @classdesc Utility for checking table inheritance relationships.
     *
     * Provides functionality to determine whether one table extends another in the ServiceNow 
     * platform. This utility helps developers understand table hierarchies and inheritance 
     * relationships when working with the database schema.
     *
     * @author Auto-Generated
     * @version 1.0.0
     */
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
 * @constructor
 * @description Initialise the TableExtensionUtils class
 */