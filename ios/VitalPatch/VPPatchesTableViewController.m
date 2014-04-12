//
//  VPPatchesTableView.m
//  VitalPatch
//
//  Created by Sam Toizer on 1/27/14.
//  Copyright (c) 2014 Northwestern University. All rights reserved.
//

#import "VPPatchesTableViewController.h"
#import "VPPatchViewController.h"
#import "VPPatch.h"

@implementation VPPatchesTableViewController

@synthesize patches;

- (id) init {
    self = [super init];
    if (self) {
        self.title = @"Patches";
    }
    
    return self;
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    
    self.patches = [[NSMutableArray alloc] init];
    
    // Dummy data
    // Dad
    VPPatch* dad = [[VPPatch alloc] init];
    dad.name = @"Dad";
    dad.temp = @"96.7˚F";
    dad.pulse = @"120bpm";
    [patches addObject:dad];
    
    // Mom
    VPPatch* mom = [[VPPatch alloc] init];
    mom.name = @"Mom";
    mom.temp = @"99.6˚F";
    mom.pulse = @"143bpm";
    [patches addObject:mom];
}

#pragma mark - UITableViewDelegate
- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return self.patches.count;
}

- (UITableViewCell*)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    VPPatch* patch = [self.patches objectAtIndex:indexPath.row];
    
    UITableViewCell* cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:nil];
    cell.textLabel.text = patch.name;
    cell.accessoryType = UITableViewCellAccessoryDisclosureIndicator;
    
    return cell;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    VPPatch* patch = [self.patches objectAtIndex:indexPath.row];
    VPPatchViewController* patchVC = [[VPPatchViewController alloc] initWithPatch:patch];
    [self.navigationController pushViewController:patchVC animated:YES];
}


// Custom format cells
- (void)tableView:(UITableView *)tableView willDisplayCell:(UITableViewCell *)cell forRowAtIndexPath:(NSIndexPath *)indexPath {
    cell.backgroundColor = [UIColor whiteColor];
}

@end

