/**
 * Checks if a child table extends a parent table
 * 
 * @param {string} parent - The name of the parent table
 * @param {string} child - The name of the child table to check
 * @returns {boolean} True if the child table extends the parent table, false otherwise
 */
function isTableExtended(parent, child){
    gs.include("j2js");
    /**
     * @class isTableExtended
     * @classdesc Determines if a child table extends a parent table.
     *
     * This utility function checks the table hierarchy to verify if a specified child table
     * is an extension of a given parent table. It uses TableUtils to examine the table structure
     * and returns a boolean result indicating the relationship between the tables.
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
 * @description Initialise the isTableExtended class
 */