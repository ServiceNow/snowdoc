/**
 * @function isTableExtended
 * @description Checks if a specified child table is extended from a specified parent table.
 *
 * This function utilizes the TableUtils API to first check if the parent table exists and has extensions,
 * then retrieves its extensions and checks if the child table name is present in the list.
 *
 * @param {string} parent - The name of the potential parent table.
 * @param {string} child - The name of the potential child table.
 * @returns {boolean} True if the child table is extended from the parent, false otherwise. Returns false if the parent table doesn't exist or has no extensions.
 */
function isTableExtended(parent, child){
    gs.include("j2js");
    /**
     * @class TableUtilsHelper
     * @classdesc Provides helper functions for interacting with table extensions.
     *
     * This Script Include wraps common operations related to checking table hierarchies and extensions using the server-side TableUtils API.
     * It can be used in various server-side scripts (Business Rules, Script Includes, etc.) to quickly determine if one table is extended from another.
     * Use this class when you need to programmatically verify table relationships in your ServiceNow instance.
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
 * @description Initialise the TableUtilsHelper class
 */